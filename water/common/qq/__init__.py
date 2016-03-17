# coding=utf-8
import json
import re
from common import REG_FOR_JSON

SAVE_FILE = 'qq/'

PLATFORM = 'qq'


def get_playlist(json_content):
    if not json_content.get('list'):
        return
    recicle_time = 1
    for _ in json_content.get('list'):
        tv_type = _.get('BC')
        if tv_type not in [u'电视剧', u'综艺']:
            match = re.search(u'[\u4e00-\u9fa5]+', tv_type)
            tv_type = match and match.group() or ''
        if _.get('PLNAME') != u'qq' or tv_type not \
           in [u'电视剧', u'综艺'] or _.get('BE') in [u'片花']:
            if not recicle_time:
                return
            else:
                recicle_time -= 1
                continue
        else:
            return _

    tmp_playlist = json_content.get('list')[0]
    if tmp_playlist.get('PLNAME') != u'qq' or tmp_playlist.get('BC') not \
       in [u'电视剧', u'综艺'] or tmp_playlist.get('BE') in [u'片花']:
        return
    else:
        return tmp_playlist


def play_info_is_valid_qq(page):
    if not page:
        return
    try:
        json_content = json.loads(re.search(REG_FOR_JSON, page).group())
    except:
        return
    return json_content


def tv_info_is_valid_qq(page):
    if not page:
        return
    try:
        json_content = json.loads(re.search(REG_FOR_JSON, page).group())
    except:
        return
    play_list = get_playlist(json_content)
    if not play_list:
        return
    try:
        src_play_list = play_list['src_list']['vsrcarray'][0]['playlist']
        vsrcarray = play_list['src_list']['vsrcarray'][0]
    except:
        return
    if not (src_play_list or vsrcarray):
        return
    return json_content


def get_all_list(src_play_list):
    all_list = []
    if isinstance(src_play_list, dict):
        for _ in src_play_list.values():
            all_list.extend(_)
    else:
        all_list = src_play_list
    return all_list
