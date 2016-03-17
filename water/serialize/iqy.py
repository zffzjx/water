# coding=utf-8
import re
from cg_core import utils
from handler.model import (
    # PlayInfo,
    TvInfo,
)
from spider import request
from common.iqy import tv_info_is_valid
from common.iqy import PLATFORM


class Iqy(object):

    def dianshiju_info(self, tv_infos, db_tv_names):
        url = u'http://cache.video.qiyi.com/jp/vi/{}/{}/'
        for name, tv_info in tv_infos.items():
            warning_message = u"《{}》tv_info ,结果不准确\r\n". \
                              format(name)
            tv_id = tv_info[1]['id']
            vids = tv_id
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

    def zongyi_info(self, tv_infos, db_tv_names):
        url = u'http://cache.video.qiyi.com/jp/vi/{}/{}/'
        for name, tv_info in tv_infos.items():
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

    def play_info(self):
        url = 'http://mixer.video.iqiyi.com/jp/mixin/videos/{}/'
