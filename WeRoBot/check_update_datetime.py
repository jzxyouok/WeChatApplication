# -*- coding: utf-8 -*-
import os
import re
import time
import urllib2

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WeRoBot.settings")


def parse_update_data(html):
    soup_outer = BeautifulSoup(html, "lxml", from_encoding="utf-8")
    for tr in soup_outer.find_all(name="tr")[1:]:
        td = tr.find_all(name="td")
        film = td[0].get_text().strip()
        developer = td[1].get_text().strip()
        dilution = td[2].get_text().strip()
        asa_iso = td[3].get_text().strip()
        a35mm = td[4].get_text().strip()
        a120 = td[5].get_text().strip()
        sheet = td[6].get_text().strip()
        temp = td[7].get_text().strip()
        try:
            notes_link = td[8].find(name="a").get("href")
            notes_link = "http://www.digitaltruth.com/"+notes_link
            notes_html = urllib2.urlopen(notes_link).read()
            soup_inner = BeautifulSoup(notes_html, "lxml", from_encoding="utf8")
            notes = soup_inner.find_all(name="tr")[1].find_all(name="td")[-1].get_text().strip()
        except AttributeError:
            notes = ""
        from myrobot.models import FilmSearch
        try:
            obj = FilmSearch.objects.get(Film=film, Developer=developer, Dilution=dilution,
                                         ASA_ISO=asa_iso, Temp=temp)
            obj.a35mm = a35mm
            obj.a120 = a120
            obj.sheet = sheet
            obj.Notes = notes
            obj.save()
        except FilmSearch.DoesNotExist:
            obj = FilmSearch(Film=film, Developer=developer, Dilution=dilution, ASA_ISO=asa_iso,
                             a35mm=a35mm, a120=a120, sheet=sheet, Notes=notes)
            obj.save()


if __name__ == '__main__':
    tracked_url = "http://www.digitaltruth.com/devchart.php?doc=search"

    tracked_html = urllib2.urlopen(tracked_url).read()
    soup = BeautifulSoup(tracked_html, "lxml", from_encoding="utf8")
    last_update = soup.find_all(name="form")[1].find(name="p").get_text()
    last_update_datetime = re.findall(r":(.*?)\[", last_update, re.S)[0].strip()
    with open("last_update_datetime.txt", "r+") as fp:
        stored_datetime = fp.read().strip()
        if last_update_datetime != stored_datetime:
            fp.seek(0)
            fp.write(last_update_datetime)
            try:
                driver = webdriver.PhantomJS()
                try:
                    driver.get("http://www.digitaltruth.com/devchart.php?doc=search")
                    try:
                        last_update_link = WebDriverWait(driver, 10).until(
                            expected_conditions.presence_of_element_located((By.NAME, "idForm"))
                        )
                        last_update_link.click()
                        time.sleep(2)
                        parse_update_data(driver.page_source)
                    except NoSuchElementException, e:
                        raise e
                except TimeoutException, e:
                    raise e
            except WebDriverException, e:
                raise e
