# coding=utf-8
import time
import re
from spider import request
from cg_core import utils
from common.yk import (
    info_and_play_is_valid,
    PLATFORM
)
from handler.model import (
    PlayInfo,
    TvInfo,
)


class Yk(object):

    def __init__(self, now):
        self.now = now

    def info_and_play(self, tv_urls_map, db_tv_names, db_play_info_map):
        for name, url in tv_urls_map.items():
            warning_message = u"yk 《{} 》结果不准确\r\n". \
                              format(name)
            page = request(url)
            content = info_and_play_is_valid(page, name)
            if not content:
                time.sleep(30)
                page = request(url)
                content = info_and_play_is_valid(page, name)
            if not content:
                utils.log(message=warning_message)
                continue
            last_update_time = ''
            label = ''
            update_info = ''
            detail_urls = url
            detail_titles = ''
            detail_episodes = ''
            tv_id = re.search(u'id.+?\.html', url).group()[:-5]
            title_str = re.search(u'<h1 class="title">(.|\n)+?</h1>', page). \
                group()
            tv_type = re.search(u'target="_blank">.+?<', title_str). \
                group()[16:-1]
            cast_member = []
            cast_member_flag = u'主持人' if tv_type == u'综艺' else u'主演'
            cast_member_str = re.search(
                cast_member_flag + u':</label>(.|\n)+?</span>', page).group()
            for m in re.finditer(u'<a.+?</a>', cast_member_str):
                cast_member.append(re.search('">.+?<', m.group()).group()[2:-1]) # noqa
            cast_member = ",".join(cast_member)
            description_str = re. \
                search(u'<span class="short" id="show_info_short"(.|\n)+?</div>', content).group() # noqa
            description = re.compile(u'<.*?>|查看详情>>').sub(u'', description_str)
            all_number = ''
            current_number = ''
            if tv_type == u'电视剧':
                number_str = re.search(u'class="basenotice"(.|\n)+?<',
                                       content).group()
                current_number = re.search(u'更新至\d+', number_str)
                all_number = re.search(u'共\d+', number_str).group()[1:]
                current_number = current_number and current_number.group()[3:] or all_number # noqa
            if tv_type == u'综艺':
                all_number = 0
                tmp_episode = []
                for _ in re.finditer(u'y\.episode\.show\(\'.+?\'\)', content):
                    number_url = 'http://www.youku.com/show_episode/{}.html?dt=json&divid={}' # noqa
                    divid = re.search(u'\'.+?\'', _.group()).group()[1:-1]
                    current_number_str = request(number_url.format(tv_id.encode('utf8'), divid.encode('utf8'))) # noqa
                    if not current_number_str:
                        warning_message = u"yk 《{} 》number结果不准确\r\n". \
                            format(name)
                        utils.log(message=warning_message)
                        continue
                    tmp_episode = [_ for _ in re.finditer(u'<ul(.|\n)+?</ul>',
                                                          current_number_str)]
                    all_number += len(tmp_episode)
                if not all_number:
                    tmp_episode = re.search(u'<div id="episode">(.|\n)+?</div>', page).group() # noqa
                    tmp_episode = [_ for _ in re.finditer(u'<ul(.|\n)+?</ul>',
                                                          tmp_episode)]
                    all_number = len(tmp_episode)
                current_number = re.search(u'<label>.+?</label>',
                                           tmp_episode[0].group()).group()
                current_number = re.compile(u'<.+?>|期'). \
                    sub(u'', current_number)
            all_play_counts = re.search(u'<label>总播放:</label>.+?\n', content) \
                .group()
            all_play_counts = (int)(re.compile(u'<label>总播放:</label>|,|\n')
                                    .sub(u'', all_play_counts))
            pre_all_play_counts = db_play_info_map.get(name)
            day_play_counts = pre_all_play_counts and \
                max(all_play_counts - (int)(pre_all_play_counts), 0) or 0
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
            PlayInfo.add(
                tv_id=tv_id,
                tv_name=name,
                day_play_counts=day_play_counts,
                all_play_counts=all_play_counts,
                time_at=self.now,
                platform=PLATFORM,
                type=tv_type
            )
