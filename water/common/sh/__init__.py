# coding=utf-8
import re
import json

SH_REG_FOR_JSON = u'{"(.|\n)*}'

SAVE_FILE = 'sh/'

PLATFORM = 'sh'

TV_TYPE_MAP = {
    2: u'电视剧',
    7: u'综艺',
}


def info_is_valid(page):
    if not page:
        return
    json_content = None
    try:
        json_content = json.loads(re.search(SH_REG_FOR_JSON, page).group())
        if json_content['cid'] not in TV_TYPE_MAP.keys():
            return
    except:
        return
    return json_content


def play_is_valid(page, pid):
    if not page:
        return
    json_content = None
    try:
        json_content = json.loads(re.search(SH_REG_FOR_JSON, page).group()[:-1]) # noqa
        if not json_content[pid]['total']:
            return
    except:
        return
    return json_content
