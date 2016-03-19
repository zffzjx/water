# coding=utf-8
from common import REG_FOR_JSON
import json
import re

SAVE_FILE = 'iqy/'

PLATFORM = 'iqy'


def tv_info_is_valid(page):
    if not page:
        return
    try:
        json_content = json.loads(re.search(REG_FOR_JSON, page).group())
    except:
        return
    try:
        if not json_content['es']:
            return
    except:
        return
    return json_content


def play_info_is_valid(page):
    if not page:
        return
    try:
        json_content = json.loads(re.search(REG_FOR_JSON, page).group())
    except:
        return
    try:
        if not json_content['playCount']:
            return
    except:
        return
    return json_content
