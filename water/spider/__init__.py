# coding=utf-8
import requests
import time
from cg_core import utils
import json
import re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'} # noqa
REG_FOR_JSON = u'{(.|\n)*}'


def request(url, interval=60, cycle_times=3):
    """
    Result for request target url.

    return unicode  type result

    error return None.
    """
    while(cycle_times):
        try:
            result = requests.get(url, headers=headers)
            if result.status_code == 200:
                result.encoding = 'utf8'
                return result.text
            if result.status_code == 500:
                time.sleep(interval)
        except:
            utils.log(name='qq', message="网络出现错误,{}秒之后会重新抓取\r\n".format(interval)) # noqa
            result = None
        cycle_times -= 1
    return result


def get_playlist(json_content):
    if not json_content.get('list'):
        return
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
