# coding=utf-8
import re
import json
from common import REG_FOR_JSON

SAVE_FILE = 'let/'

PLATFORM = 'let'


def dianshiju_is_valid(page):
    if not page:
        return
    try:
        re.search(u'<p class="p7">(.|\n)+?</p>', page).group()
        re.search(u'共\d+?集', page).group()
    except:
        return
    return page


def play_info_is_valid(page):
    if not page:
        return
    json_content = None
    try:
        json_content = json.loads(re.search(REG_FOR_JSON, page).group())
    except:
        return
    if not json_content:
        return
    return json_content


def zongyi_is_valid(page):
    if not page:
        return
    try:
        re.search(u'pid: \d+?', page)
    except:
        return
    return page


def description_is_valid(page):
    if not page:
        return
    try:
        re.search(u'<p class="p7">(.|\n)+?</p>', page).group()
    except:
        return
    return page


def number_utl_is_valid(page):
    if not page:
        return
    json_content = None
    try:
        json_content = json.loads(re.search(REG_FOR_JSON, page).group())
        if not json_content['data']:
            return
    except:
        return
    return json_content
