# coding=utf-8
from spider import request
from cg_core import utils
from common.sh import (
    PLATFORM,
    TV_TYPE_MAP,
    info_is_valid,
    play_is_valid
)
from handler.model import (
    PlayInfo,
    TvInfo,
)


class Sh(object):

    def __init__(self, now):
        self.now = now

    def info_and_play(self, pids_map, db_tv_names, db_play_info_map):
        play_url = 'http://count.vrs.sohu.com/count/queryext.action?plids={}&callback=callback' # noqa
        info_url = 'http://pl.hd.sohu.com/videolist?playlistid={}&callback=callback' # noqa
        for name, pid in pids_map.items():
            tv_id = pid
            info = request(info_url.format(pid.encode('utf8')))
            json_content = info_is_valid(info)
            if not json_content:
                warning_message = u"sh《{}》tv_info ,结果不准确\r\n". \
                    format(name)
                utils.log(message=warning_message)
                continue
            description = json_content['albumDesc']
            last_update_time = ''
            current_number = json_content['updateSet']
            all_number = json_content['totalSet']
            all_number = all_number != u'0' and all_number or current_number
            tv_type = TV_TYPE_MAP.get(json_content['cid'])
            if tv_type == u'综艺':
                cast_member = json_content['hosts']
            else:
                cast_member = json_content['actors']
            cast_member = u",".join(cast_member)
            label = ",".join(json_content['categories'])
            update_info = json_content['updateNotification']
            detail_urls = ''
            detail_titles = ''
            detail_episodes = ''
            play = request(play_url.format(pid.encode('utf8')))
            play_json = play_is_valid(play, pid)
            if not play_json:
                warning_message = u"sh《{}》play_info ,结果不准确\r\n". \
                    format(name)
                utils.log(message=warning_message)
                continue
            all_play_counts = play_json[pid]['total']
            pre_all_play_counts = db_play_info_map.get(name)
            day_play_counts = pre_all_play_counts and \
                max(all_play_counts - (int)(pre_all_play_counts), 0) or 0
            if name in db_tv_names:
                TvInfo.update(name=name, tv_id=pid,
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
            PlayInfo.add(
                tv_id=tv_id,
                tv_name=name,
                day_play_counts=day_play_counts,
                all_play_counts=all_play_counts,
                time_at=self.now,
                platform=PLATFORM,
                type=tv_type
            )
