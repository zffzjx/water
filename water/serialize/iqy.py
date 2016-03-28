# coding=utf-8
import time
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
            warning_message = u"《iqy {}》tv_info ,结果不准确\r\n". \
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
        for name, tv_info in tv_infos.items():
            # print u"抓取《{}》中".format(name)
            tv_id = u''
            description = tv_info[2]
            last_update_time = u''
            all_number = len(tv_info[0])
            current_number = tv_info[1]
            cast_member = tv_info[3]
            label = u''
            update_info = u''
            detail_urls = u''
            vids = ",".join(tv_info[0])
            tv_type = u'综艺'
            detail_titles = u''
            detail_episodes = u''
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
            tmp_all_play_counts = 0
            for vid in db_tv_info.vids.split(','):
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
