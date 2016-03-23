# coding=utf-8
import re
from common.let import PLATFORM
from spider import request
from common.let import (
    dianshiju_is_valid,
    play_info_is_valid,
    zongyi_is_valid,
    description_is_valid,
    number_utl_is_valid
)
from handler.model import (
    PlayInfo,
    TvInfo,
)


class Let(object):
    def __init__(self, now):
        self.now = now

    def dianshiju(self, urls_map, db_tv_names, db_play_info_map):
        play_url = 'http://v.stat.letv.com/vplay/queryMmsTotalPCount?callback=callback&pid={}' # noqa
        for name, tv_info in urls_map.items():
            url = tv_info[0]
            pid = tv_info[1]
            tv_id = pid
            cast_member = tv_info[2]
            last_update_time = u''
            update_info = u''
            detail_urls = url
            tv_type = u'电视剧'
            detail_titles = u''
            detail_episodes = u''
            label = tv_info[3]
            page = request(url)
            content = dianshiju_is_valid(page)
            if not content:
                continue
            description = re.search(u'<p class="p7">(.|\n)+?</p>', content). \
                group()
            description = re.compile(u'<.+?>').sub('', description)
            all_number = re.search(u'共\d+?集', content).group()
            current_number = re.search(u'至\d+?集', content)
            current_number = current_number and current_number.group() or \
                all_number

            page = request(play_url.format(pid))
            json_content = play_info_is_valid(page)
            if not json_content:
                continue
            all_play_counts = json_content.get('plist_play_count')
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

    def zongyi(self, urls_map, db_tv_names, db_play_info_map):
        pids = []
        number_utl = 'http://api.le.com/mms/out/album/videos?id={}&cid=11&platform=pc&callback=callback' # noqa
        play_url = 'http://v.stat.letv.com/vplay/queryMmsTotalPCount?callback=callback&pid={}' # noqa
        description_url = 'http://www.le.com/zongyi/{}.html'
        for name, tv_info in urls_map.items():
            url = tv_info[0]
            label = tv_info[1]
            pid_page = request(url)
            pid_page = zongyi_is_valid(pid_page)
            if not pid_page:
                continue
            pid = re.search(u'pid: \d+?,', pid_page).group()
            pid = re.search(u'\d+', pid).group()
            if pid in pids:
                continue
            pids.append(pid)
            tv_id = pid
            d_page = request(description_url.format(pid.encode('utf8')))
            d_page = description_is_valid(d_page)
            if not d_page:
                continue
            description = re.search(u'<p class="p7">(.|\n)+?</p>', d_page). \
                group()
            description = re.compile(u'<.+?>').sub('', description)

            last_update_time = u''
            update_info = u''
            detail_urls = url
            tv_type = u'综艺'
            detail_titles = u''
            detail_episodes = u''

            n_page = request(number_utl.format(pid))
            n_json = number_utl_is_valid(n_page)
            if not n_json:
                continue
            all_number = n_json['total']
            current_number = n_json['data'][0]['episode']
            cast_member = []
            [cast_member.append(_.get('guest')) for _ in n_json['data']]
            # remove repeat
            cast_member = " ".join(cast_member)
            cast_member = cast_member.split(" ")
            cast_member = list(set(cast_member))
            cast_member = " ".join(cast_member)

            page = request(play_url.format(pid))
            json_content = play_info_is_valid(page)
            if not json_content:
                continue
            all_play_counts = json_content.get('plist_play_count')
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
