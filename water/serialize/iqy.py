# coding=utf-8
import re
from cg_core import utils
from handler.model import (
    PlayInfo,
    TvInfo,
)
from spider import request
from common.iqy import (
    tv_info_is_valid,
    play_info_is_valid
)
from common.iqy import PLATFORM


class Iqy(object):

    def __init__(self, now):
        self.now = now

    def dianshiju_info(self, tv_infos, db_tv_names):
        url = u'http://cache.video.qiyi.com/jp/vi/{}/{}/'
        for name, tv_info in tv_infos.items():
            # print u"抓取《{}》中".format(name)
            warning_message = u"《{}》tv_info ,结果不准确\r\n". \
                              format(name)
            tv_id = tv_info[1]['id']
            vids = tv_info[2]['v_id']
            page = request(url.format(tv_id, vids))
            json_content = tv_info_is_valid(page)
            if not json_content:
                utils.log(message=warning_message)
                continue
            all_number = json_content['es']
            current_number = json_content['upOrder']
            description = json_content['info']
            label = json_content['tg']
            cast_member = json_content['ma']
            update_info = json_content['qiyiPlayStrategy'][:32]
            last_update_time = json_content['up']
            detail_urls = tv_info[0]['url']
            tv_type = u'电视剧'
            detail_titles = json_content['vn']
            detail_episodes = ''
            if name in db_tv_names:
                TvInfo.update(name=name, tv_id=tv_id,
                              description=description,
                              last_update_time=last_update_time,
                              all_number=all_number,
                              current_number=current_number,
                              cast_member=cast_member,
                              platform=PLATFORM,
                              label=label, update_info=update_info,
                              detail_urls=detail_urls,
                              vids=tv_id,
                              type=tv_type,
                              detail_titles=detail_titles,
                              detail_episodes=detail_episodes,
                              )
            else:
                TvInfo.add(name=name, tv_id=tv_id,
                           description=description,
                           last_update_time=last_update_time,
                           all_number=all_number,
                           current_number=current_number,
                           cast_member=cast_member, platform=PLATFORM,
                           label=label, update_info=update_info,
                           detail_urls=detail_urls, vids=tv_id,
                           type=tv_type,
                           detail_titles=detail_titles,
                           detail_episodes=detail_episodes,
                           )

    def zongyi_info(self, tv_infos, db_tv_names):
        url = u'http://cache.video.qiyi.com/jp/vi/{}/{}/'
        for name, tv_info in tv_infos.items():
            # print u"抓取《{}》中".format(name)
            json_content = {}
            current_number = ''
            detail_titles = ''
            description = ''
            vids = ''
            tv_id = ''
            label = ''
            cast_member = ''
            last_update_time = ''
            for id, v_id in zip(tv_info[1]['id'], tv_info[2]['v_id']):
                tv_id = id
                warning_message = u"《{}》{}期tv_info ,结果不准确\r\n". \
                    format(name, id)
                page = request(url.format(id, v_id))
                json_content = tv_info_is_valid(page)
                if not json_content:
                    utils.log(message=warning_message)
                    break
                tmp_current_number = re. \
                    search(u'/(\d{7,})+?', json_content['vpic']).group()[1:]
                current_number = max(tmp_current_number, current_number)
                detail_titles += json_content['vn'] + ","
                description += json_content['info'] + ","
                label = json_content['tg']
                cast_member = json_content['ma']
                tmp_last_update_time = json_content['up']
                last_update_time = max(tmp_last_update_time, last_update_time)
                update_info = json_content['qiyiPlayStrategy'][:32]
            if not json_content:
                continue
            vids = ",".join(tv_info[1]['id'])
            all_number = len(tv_info[1]['id'])
            detail_urls = ",".join(tv_info[0]['url'])
            tv_type = u'综艺'
            detail_episodes = ''
            if name in db_tv_names:
                TvInfo.update(name=name, tv_id=tv_id,
                              description=description,
                              last_update_time=last_update_time,
                              all_number=all_number,
                              current_number=current_number,
                              cast_member=cast_member,
                              platform=PLATFORM,
                              label=label, update_info=update_info,
                              detail_urls=detail_urls,
                              vids=vids,
                              type=tv_type,
                              detail_titles=detail_titles,
                              detail_episodes=detail_episodes,
                              )
            else:
                TvInfo.add(name=name, tv_id=tv_id,
                           description=description,
                           last_update_time=last_update_time,
                           all_number=all_number,
                           current_number=current_number,
                           cast_member=cast_member, platform=PLATFORM,
                           label=label, update_info=update_info,
                           detail_urls=detail_urls, vids=vids,
                           type=tv_type,
                           detail_titles=detail_titles,
                           detail_episodes=detail_episodes,
                           )

    def play_info(self, db_play_info_map, db_tv_infos):
        url = 'http://mixer.video.iqiyi.com/jp/mixin/videos/{}/'
        for db_tv_info in db_tv_infos:
            # print u'《{}》play_info 抓取中'.format(db_tv_info.name)
            day_play_counts = 0
            all_play_counts = 0
            for vid in db_tv_info.vids.split(','):
                warning_message = u"《{}》{} play_info ,结果不准确\r\n". \
                    format(db_tv_info.name, vid)
                page = request(url.format(vid))
                json_content = play_info_is_valid(page)
                if not json_content:
                    # print u'《{}》play_info 抓取失败'.format(db_tv_info.name)
                    utils.log(message=warning_message)
                    continue
                tmp_all_play_counts = (int)(json_content['playCount'])
                pre_all_play_counts = db_play_info_map.get(db_tv_info.name)
                tmp_day_play_counts = pre_all_play_counts and \
                    max(all_play_counts - (int)(pre_all_play_counts), 0) or 0
                day_play_counts += (int)(tmp_day_play_counts)
                all_play_counts += (int)(tmp_all_play_counts)
            PlayInfo.add(
                tv_id=vid,
                tv_name=db_tv_info.name,
                day_play_counts=day_play_counts,
                all_play_counts=all_play_counts,
                time_at=self.now,
                platform=PLATFORM,
                type=db_tv_info.type
            )
