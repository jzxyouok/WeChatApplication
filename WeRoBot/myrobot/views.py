# -*- coding: utf-8 -*-
import json
import re
import requests
import urllib2

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import *
from wechat_sdk.messages import *
from wechat_sdk.context.framework.django import DatabaseContextStore

from models import FilmSearch, Films, Notes

conf = WechatConf(
    token='ggfilm',
    appid='wxd215ea1905032a90',
    appsecret='14a0dc6d2dc81db94f46f2755f0f4702',
    encrypt_mode='normal',
    encoding_aes_key='N0iYQ4h7yucFJdtQIxXdM4SjKG1VBErCuNSnY5DHebb',
)

menu = {
    'button':[
        {
            'type': 'view',
            'name': '搜索参数',
            'url': 'http://www.fotolei.cn/search'
        },
        {
            'name': 'F1冲洗机',
            'sub_button': [
                {
                    'type': 'click',
                    'name': '入门视频教程',
                    'key': ''
                },
            ]
        },
        {
            'name': '胶片教程',
            'sub_button': [
                {
                    'type': 'click',
                    'name': '胶片存放',
                    'key': ''
                },
            ]
        }
    ]
}

wechat = WechatBasic(conf=conf)


@csrf_exempt
def index(request):
    if request.method == 'GET':
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        if not wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest("Failed!")
        return HttpResponse(request.GET.get('echostr', ''), content_type="text/plain")

    try:
        wechat.create_menu(menu_data=menu)
    except OfficialAPIError:
        return HttpResponseBadRequest('Failed to Create Menu')

    try:
        wechat.parse_data(request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid Body Text')    

    if isinstance(wechat.message, EventMessage):
        xml = wechat.response_text(content='感谢您关注龟龟摄影微信公众号！回复【历史消息】，查看往期推送信息；') 
        return HttpResponse(xml, content_type='application/xml')
    if isinstance(wechat.message, TextMessage):
        content = wechat.message.content.strip()
        if content == u'历史消息':
            access_token_response = urllib2.urlopen(
                'https://api.weixin.qq.com/cgi-bin/token?grant_type'
                '=client_credential&appid=wxd215ea1905032a90&secret=14a0dc6d2dc81db94f46f2755f0f4702').read()
            access_token = json.loads(access_token_response).get('access_token')
            post_url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s' % access_token
            post_data = json.dumps({'type': "news", 'offset': 0, 'count': 4})
            response = requests.post(post_url, data=post_data).json()
            item_count = int(response["item_count"])
            media_id_list = []
            for j in range(item_count):
                media_id = response["item"][j]["media_id"]
                media_id_list.append(media_id)
            news_item_list = []

            for media_id in media_id_list:
                post_url = 'https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=%s' % access_token   
                post_data = json.dumps({'media_id': media_id})
                response = requests.post(post_url, data=post_data).json()
                news_item_list.append((response["news_item"][0]["title"].encode("raw_unicode_escape"),
                                       response["news_item"][0]["thumb_url"].encode("raw_unicode_escape"),
                                       response["news_item"][0]["url"].encode("raw_unicode_escape")))
            
            articles = []
            for j in range(item_count):
                articles.append({'title': news_item_list[j][0],
                                 'picurl': news_item_list[j][1],
                                 'url': news_item_list[j][2]})
            xml = wechat.response_news(articles)
            return HttpResponse(xml, content_type='application/xml')


def update_database(request):
    return render(request, "update.html")


def search_database_film(request):
    films = Films.objects.all().order_by("Film")

    display_35mm = []
    for film in films:
        if FilmSearch.objects.filter(Film=film.Film).exclude(a35mm="").exists():
            display_35mm.append(FilmSearch.objects.filter(Film=film.Film).exclude(a35mm="")[0].Film)
    display_35mm_counts = len(display_35mm)

    display_120 = []
    for film in films:
        if FilmSearch.objects.filter(Film=film.Film).exclude(a120="").exists():
            display_120.append(FilmSearch.objects.filter(Film=film.Film).exclude(a120="")[0].Film)
    display_120_counts = len(display_120)

    display_sheet = []
    for film in films:
        if FilmSearch.objects.filter(Film=film.Film).exclude(Sheet="").exists():
            display_sheet.append(FilmSearch.objects.filter(Film=film.Film).exclude(Sheet="")[0].Film)
    display_sheet_counts = len(display_sheet)

    return render(request, "search_film.html", {"display_35mm": display_35mm,
                                                "display_35mm_counts": display_35mm_counts,
                                                "display_120": display_120,
                                                "display_120_counts": display_120_counts,
                                                "display_sheet": display_sheet,
                                                "display_sheet_counts": display_sheet_counts})


def search_database_developer(request):
    source = request.GET.get("source")
    film = request.GET.get("film").replace('^', '+')
    films_search = None
    if source == "135":
        films_search = FilmSearch.objects.filter(Film=film).exclude(a35mm="")
    elif source == "120":
        films_search = FilmSearch.objects.filter(Film=film).exclude(a120="")
    elif source == u"页片":
        films_search = FilmSearch.objects.filter(Film=film).exclude(Sheet="")
    display_developer = []
    for film_search in films_search:
        if film_search.Developer not in display_developer:
            display_developer.append(film_search.Developer)
    display_developer_counts = len(display_developer)
    return render(request, "search_developer.html", {"nav": {"source": source, "film": film},
                                                     "display_developer": display_developer,
                                                     "display_developer_counts": display_developer_counts})


def search_database_dilution(request):
    source = request.GET.get("source")
    film = request.GET.get("film").replace('^', '+')
    developer = request.GET.get("developer").replace('^', '+')
    films_search = None
    if source == "135":
        films_search = FilmSearch.objects.filter(Film=film).exclude(a35mm="").filter(Developer=developer)
    elif source == "120":
        films_search = FilmSearch.objects.filter(Film=film).exclude(a120="").filter(Developer=developer)
    elif source == u"页片":
        films_search = FilmSearch.objects.filter(Film=film).exclude(Sheet="").filter(Developer=developer)
    display_dilution = []
    for film_search in films_search:
        if film_search.Dilution not in display_dilution:
            display_dilution.append(film_search.Dilution)
    display_dilution_counts = len(display_dilution)
    return render(request, "search_dilution.html", {"nav": {"source": source, "film": film, "developer": developer},
                                                    "display_dilution": display_dilution,
                                                    "display_dilution_counts": display_dilution_counts})


def search_database_asa_iso(request):
    source = request.GET.get("source")
    film = request.GET.get("film").replace('^', '+')
    developer = request.GET.get("developer").replace('^', '+')
    dilution = request.GET.get("dilution").replace('^', '+')
    films_search = None
    if source == "135":
        films_search = FilmSearch.objects.filter(Film=film).exclude(a35mm="").filter(Developer=developer).filter(Dilution=dilution)
    elif source == "120":
        films_search = FilmSearch.objects.filter(Film=film).exclude(a120="").filter(Developer=developer).filter(Dilution=dilution)
    elif source == u"页片":
        films_search = FilmSearch.objects.filter(Film=film).exclude(Sheet="").filter(Developer=developer).filter(Dilution=dilution)
    display_asa_iso = []
    for film_search in films_search:
        if film_search.ASA_ISO not in display_asa_iso:
            display_asa_iso.append(film_search.ASA_ISO)
    display_asa_iso_counts = len(display_asa_iso)
    return render(request, "search_asa_iso.html", {"nav": {"source": source, "film": film, "developer": developer,
                                                           "dilution": dilution},
                                                   "display_asa_iso": display_asa_iso,
                                                   "display_asa_iso_counts": display_asa_iso_counts})


def search_database_result(request):
    source = request.GET.get("source")
    film = request.GET.get("film").replace('^', '+')
    developer = request.GET.get("developer").replace('^', '+')
    dilution = request.GET.get("dilution").replace('^', '+')
    asa_iso = request.GET.get("asa_iso").replace('^', '+')
    result = None
    if source == "135":
        result = FilmSearch.objects.filter(Film=film).exclude(a35mm="").filter(Developer=developer).filter(Dilution=dilution).filter(ASA_ISO=asa_iso)[0]
    elif source == "120":
        result = FilmSearch.objects.filter(Film=film).exclude(a120="").filter(Developer=developer).filter(Dilution=dilution).filter(ASA_ISO=asa_iso)[0]
    elif source == u"页片":
        result = FilmSearch.objects.filter(Film=film).exclude(Sheet="").filter(Developer=developer).filter(Dilution=dilution).filter(ASA_ISO=asa_iso)[0]

    time = ""
    if source == "135":
        time = result.a35mm
    elif source == "120":
        time = result.a120
    elif source == u"页片":
        time = result.Sheet

    temperature = result.Temp.split("C")[0]

    note_list = []
    if result.Notes != "":
        note_orders = result.Notes
        note_orders = re.findall(r"\[(.*?)\]", note_orders)
        for note_order in note_orders:
            if note_order == "46":
                pass
            else:
                note = Notes.objects.get(Notes=note_order).Remark
                note_list.append(note)
    has_note = len(note_list)
    return render(request, "search_result.html", {"nav": {"source": source, "film": film, "developer": developer,
                                                          "dilution": dilution, "asa_iso": asa_iso},
                                                  "time": time,
                                                  "temperature": temperature,
                                                  "has_note": has_note,
                                                  "note_list": note_list})
