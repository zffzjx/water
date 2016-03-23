# coding=utf-8
import re
from spider import request
from common.mg import (
    PLATFORM,
    TV_TYPE_MAP,
    info_is_valid,
    number_info_is_valid,
    year_json_is_valid,
    play_is_valid
)
from handler.model import (
    PlayInfo,
    TvInfo,
)


class Mg(object):

    def __init__(self, now):
        self.now = now

    def info_and_play(self, pids_map, db_tv_names, db_play_info_map):
        play_url = 'http://videocenter-2039197532.cn-north-1.elb.amazonaws.com.cn/dynamicinfo?callback=callback&cid={}' # noqa
        info_url = 'http://www.mgtv.com/v/{type_n}/{pid}'
        year_url = 'http://www.mgtv.com/v/1/{}/s/json.year.js'
        number_url = 'http://www.mgtv.com/v/1/{pid}/s/json.{year}.js'
        for name, tv_infos in pids_map.items():
            pid = tv_infos[0].encode('utf8')
            tv_id = pid
            info = request(info_url.format(type_n=tv_infos[1], pid=tv_infos[0])) # noqa
            info = info_is_valid(info)
            if not info:
                continue
            last_update_time = ''
            update_info = ''
            detail_urls = ''
            detail_titles = ''
            detail_episodes = ''
            current_number = re.search(u'"series" : ".+?"', info).group()
            current_number = current_number.split(':')[1][2:-1]
            description = re.search(u'简介</em>(.|\n)+?</span>', info).group()
            description = re.compile(u'<.+?>|简介|：|\s').sub(u'', description)
            tv_type = TV_TYPE_MAP[tv_infos[1]]
            cast_flag = u'主演' if tv_type == u'电视剧' else u'主持人'
            cast_member = re.search(u'{}</em>(.|\n)+?</p>'.format(cast_flag),
                                    info).group()
            cast_member = re.compile(u'<.+?>|主演|主持人|：').sub(u'', cast_member)
            label = re.search(u'类型</em>(.|\n)+?</p>', info).group()
            label = re.compile(u'<.+?>|类型|：|\s').sub(u'', label)
            if tv_type == u'电视剧':
                all_number = re.search(u'共<b>\d+?</b>集', info).group()
                all_number = re.search(u'\d+', all_number).group()
            else:
                year_json = request(year_url.format(pid))
                year = year_json_is_valid(year_json)
                if not year:
                    continue
                number_info = request(number_url.format(pid=pid,
                                      year=(int)(year[0])))
                number_info = number_info_is_valid(number_info)
                if not number_info:
                    continue
                all_number = len([_ for _ in number_info])
            play_info = request(play_url.format(pid))
            play_json = play_is_valid(play_info)
            if not play_json:
                break
            all_play_counts_str = play_json['data']['allVVStr']
            all_play_counts = (float)(re.compile(u'万|亿').sub(u'', all_play_counts_str)) # noqa
            if u'万'in all_play_counts_str:
                all_play_counts *= 10000
            elif u'亿'in all_play_counts_str:
                all_play_counts *= 100000000
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
