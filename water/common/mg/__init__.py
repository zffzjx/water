# coding=utf-8
import re
import json

MG_REG_FOR_JSON = u'\[(.|\n)*\]'
MG_REG_FOR_JSON_2 = u'{(.|\n)*\}'

SAVE_FILE = 'mg/'

PLATFORM = 'mg'

TV_TYPE_MAP = {
    1: u'综艺',
    2: u'电视剧'
}


def info_is_valid(page):
    if not page:
        return
    try:
        re.search(u'"series" : ".+?"', page).group()
    except:
        return
    return page


def play_is_valid(page):
    if not page:
        return
    json_content = None
    try:
        json_content = json.loads(re.search(MG_REG_FOR_JSON_2, page).group())
        if not json_content['data']['allVVStr']:
            return
    except:
        return
    return json_content


def number_info_is_valid(page):
    if not page:
        return
    json_content = None
    try:
        json_content = json.loads(re.search(MG_REG_FOR_JSON, page).group())
        if not json_content:
            return
    except:
        return
    return json_content


def year_json_is_valid(page):
    if not page:
        return
    json_content = None
    try:
        json_content = json.loads(re.search(MG_REG_FOR_JSON, page).group())
        if not json_content:
            return
    except:
        return
    return json_content
