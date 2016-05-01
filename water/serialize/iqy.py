# coding=utf-8
import time
import json
from cg_core import utils
from handler.model import (
    PlayInfo,
    TvInfo,
)
import re
from spider import (
    request,
    convert_name
)
from common.iqy import (
    play_info_is_valid,
    PLATFORM
)


class Iqy(object):

    type_map = {
        1: u'电视剧',
        2: u'综艺'
    }
    album_url = "http://iface.iqiyi.com/proxy/3.0/searchIface?key=591a3d5e95c34d3f4e2373d2df3fd506&version=6.6.1&all_episode=1&keyword={name}&type=json" # noqa
    list_url = "http://iface2.iqiyi.com/views/2.0/card_view?album_id={album_id}&page=player_tabs&fake_ids=choose_set,album_detail&plist_id=&order=&plt_full=1&full=1&plt_episode=0&fromtype=0&wts=128%2C4%2C8%2C16&wtsh=-1&core=1&app_k=591a3d5e95c34d3f4e2373d2df3fd506&app_v=6.6.1&dev_os=0.1.1&dev_ua=f*ck&dev_hw={{'country':'南极'}}&secure_p=GPhone" # noqa

    def __init__(self, now):
        self.now = now

    def info_and_play(self, names, db_tv_ids):
        for name in names:
            # print "iqy 抓取《{}》中".format(name.encode('utf8'))
            search_result = request(self.album_url.
                                    format(name=name.encode('utf8')))
            album_id = self.get_album_id(search_result)
            tv_type = self.get_type(search_result)
            if not all([tv_type, album_id]):
                continue
            lists = self.get_list(album_id)
            info = self.get_info(lists, tv_type)
            if not info:
                continue
            if album_id in db_tv_ids:
                TvInfo.update(name=info['name'], tv_id=album_id,
                              description=info['description'],
                              last_update_time='',
                              all_number=info['all_number'],
                              current_number=info['current_number'],
                              cast_member=info['cast_member'],
                              platform=PLATFORM,
                              label='', update_info='',
                              detail_urls='',
                              vids=info['vids'],
                              type=tv_type,
                              detail_titles='',
                              detail_episodes='',
                              )
            else:
                db_tv_ids.append(album_id)
                TvInfo.add(name=info['name'], tv_id=album_id,
                           description=info['description'],
                           last_update_time='',
                           all_number=info['all_number'],
                           current_number=info['current_number'],
                           cast_member=info['cast_member'],
                           platform=PLATFORM,
                           label='', update_info='',
                           detail_urls='',
                           vids=info['vids'],
                           type=tv_type,
                           detail_titles='',
                           detail_episodes='',
                           )

    def get_list(self, album_id):
        headers = {
            'User-Agent': 'QIYIVideo/6.6.1 (Gphone;com.qiyi.video;Android 0)',
            'Accept-Encoding': 'gzip',
            'sign': '851c695a4e41e90501847ddbd3094a6a',
            't': '356248956'
        }
        lists = request(self.list_url.format(album_id=album_id),
                        headers=headers)
        return lists

    def get_info(self, lists, tv_type):
        try:
            lists = json.loads(lists)
            cast_members = lists['albumIdList'][0]['items'][3]['extra']
            if cast_members:
                cast_member = u",".join([_['name'] for _ in cast_members])
            else:
                cast_member = u''
            if tv_type == u'电视剧':
                name = lists['albumIdList'][0]['current_album']['_t']
                description = lists['albumIdList'][0]['items'][-1]['text']
                description = re.compile(u'影片简介:').sub(u'', description)
                all_number = lists['albumIdList'][0]['current_album']['_tvs']
                vids = lists['albumIdList'][0]['current_album']['tv_id']
                current_number = lists['albumIdList'][0]['current_album_B']['marks']['br']['t'][:-1] # noqa
                current_number = re.search(u'\d+', current_number).group()
            else:
                name = lists['albumIdList'][0]['current_album']['clm']
                description = lists['albumIdList'][0]['items'][-1]['text']
                description = re.compile(u'本期简介:').sub(u'', description)
                blocks = lists['albumIdList'][1]['index']['float']['blocks']
                current_number = lists['albumIdList'][0]['current_album_B']['marks']['br']['t'][:-1] # noqa
                vids = []
                for block in blocks:
                    for vid in block['ids']:
                        vids.append(str(vid))
                all_number = len(vids)
                vids = ",".join(vids)
            return {
                'name': convert_name(name),
                'cast_member': cast_member,
                'description': description,
                'all_number': all_number,
                'current_number': current_number,
                'vids': vids
            }
        except:
            return

    def get_type(self, search_result):
        try:
            search_result = json.loads(search_result)
            tv_type = search_result['albumIdList'][0]['subshow_type']
            return self.type_map.get(tv_type)
        except:
            return

    def get_album_id(self, search_result):
        try:
            album = json.loads(search_result)
            album_id = album['albumIdList'][0]['items'][0]['click_event']['data']['album_id'] # noqa
            return album_id
        except:
            return

    def get_dianshiju_names(self):
        url = 'http://top.iqiyi.com/dianshiju.html'
        return [re.search(u'title=".+?"', m.group()).group()[7:-1] for m in
                re.finditer(u'<li  j-delegate="liover"(.|\n)+?</li>',
                request(url))]

    def get_zongyi_names(self):
        names = []
        url = 'http://top.iqiyi.com/index/top50.htm?cid=6&dim=day'
        for m in re.finditer(u'<li  j-delegate="liover"(.|\n)+?</li>',
                             request(url)):
            name = re.search(u'title=".+?"', m.group()).group()[7:-1]
            if u'之' in name:
                name = re.search(u'.+?之', name).group()[:-1]
            names.append(name)
        return names

    def get_names(self):
        return self.get_zongyi_names() + self.get_dianshiju_names()

    def play_info(self, db_play_info_map, db_tv_infos):
        url = 'http://mixer.video.iqiyi.com/jp/mixin/videos/{}/'
        for db_tv_info in db_tv_infos:
            # print u'《{}》play_info 抓取中'.format(db_tv_info.name)
            tmp_all_play_counts = 0
            for vid in db_tv_info.vids.split(','):
                # print u'《{}》{}期play_info 抓取中'.format(db_tv_info.name, vid)
                warning_message = u"iqy《{}》{} play_info ,结果不准确\r\n". \
                    format(db_tv_info.name, vid)
                page = request(url.format(vid))
                json_content = play_info_is_valid(page)
                if not json_content:
                    # print u'《{}》play_info 抓取失败'.format(db_tv_info.name)
                    time.sleep(30)
                    page = request(url.format(vid))
                    json_content = play_info_is_valid(page)
                if not json_content:
                    utils.log(message=warning_message)
                    continue
                tmp_all_play_counts += (int)(json_content.get('playCount'))
            all_play_counts = tmp_all_play_counts
            pre_all_play_counts = db_play_info_map.get(db_tv_info.name)
            day_play_counts = pre_all_play_counts and \
                max(all_play_counts - (int)(pre_all_play_counts), 0) \
                or 0
            PlayInfo.add(
                tv_id=vid,
                tv_name=db_tv_info.name,
                day_play_counts=day_play_counts,
                all_play_counts=all_play_counts,
                time_at=self.now,
                platform=PLATFORM,
                type=db_tv_info.type
            )
