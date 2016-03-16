# coding=utf-8
import re

from handler.model import (
    PlayInfo,
    TvInfo,
)
from cg_core import utils
from spider.qq import(
    TV_INFO_FILE_DIR,
    TV_INFO_FILE_FIX,
    PLAY_INFO_FILE_DIR,
    PLAY_INFO_FILE_FIX,
)
from spider import(
    get_all_list,
    tv_info_is_valid_qq,
    get_playlist,
    play_info_is_valid_qq
)


class Qq(object):

    PLATFORM = 'QQ'

    def __init__(self, now):
        self.now = now

    def play_info(self, db_tv_infos):
        for tv_info in db_tv_infos:
            if tv_info.type == u'综艺':
                vids = tv_info.vids.split(',')
                episodes = tv_info.detail_episodes.split(',')
                for vid, episode in zip(vids, episodes):
                    warning_message = u"《{}》第{}期play_info ,结果不准确\r\n". \
                                      format(tv_info.name, episode)

                    page = utils.read(PLAY_INFO_FILE_DIR, tv_info.name +
                                      episode + PLAY_INFO_FILE_FIX)
                    json_content = play_info_is_valid_qq(page)
                    if not json_content:
                        continue
                    try:
                        play_infos = json_content['results'][0]['fields']
                        day_play_counts = play_infos['tdnumc'] or '0'
                        all_play_counts = play_infos['allnumc'] or '0'
                    except:
                        utils.log(message=warning_message)
                        continue
                    PlayInfo.add(
                        tv_id=vid,
                        tv_name=tv_info.name,
                        day_play_counts=day_play_counts,
                        all_play_counts=all_play_counts,
                        time_at=self.now,
                        platform=self.PLATFORM,
                    )
            elif tv_info.type == u'电视剧':
                page = utils.read(PLAY_INFO_FILE_DIR, tv_info.name +
                                  PLAY_INFO_FILE_FIX)
                json_content = play_info_is_valid_qq(page)
                if not json_content:
                    continue
                try:
                    play_infos = json_content['results'][0]['fields']
                    day_play_counts = play_infos['tdnumc'] or '0'
                    all_play_counts = play_infos['allnumc'] or '0'
                except:
                    continue
                PlayInfo.add(
                    tv_id=tv_info.tv_id,
                    tv_name=tv_info.name,
                    day_play_counts=day_play_counts,
                    all_play_counts=all_play_counts,
                    time_at=self.now,
                    platform=self.PLATFORM,
                )

    def tv_info(self, tv_names, db_tv_names):
        for name in tv_names:
            page = utils.read(TV_INFO_FILE_DIR, name + TV_INFO_FILE_FIX)
            json_content = tv_info_is_valid_qq(page)
            if not json_content:
                continue
            play_list = get_playlist(json_content)
            tv_type = play_list['BC']
            description = play_list['TX']
            last_update_time = play_list['AT']
            update_info = play_list['SS']
            tv_id = play_list['ID']
            label = play_list['BE']
            cast_member = play_list['BM']

            def get_current_number(play_list):
                match = re.search('\d+-\d+-\d+', play_list['TT'])
                current_number = match and match.group()
                if not current_number:
                    match = re.search('\d+', play_list['TT'])
                    current_number = match and match.group() or ''
                return current_number
            current_number = get_current_number(play_list)

            src_play_list = play_list['src_list']['vsrcarray'][0]['playlist']
            all_list = get_all_list(src_play_list)
            vids, detail_urls, detail_titles, detail_episodes = [], [], [], []
            for _ in all_list:
                vids.append(_['id'])
                detail_urls.append(_['url'])
                detail_titles.append(_['title'])
                detail_episodes.append(_['episode_number'])
            all_number = len(vids)
            vids, detail_urls, detail_titles, detail_episodes = \
                ",".join(vids), ",".join(detail_urls), \
                ",".join(detail_titles), ",".join(detail_episodes)
            if name in db_tv_names:
                TvInfo.update(name=name, tv_id=tv_id,
                              description=description,
                              last_update_time=last_update_time,
                              all_number=all_number,
                              current_number=current_number,
                              cast_member=cast_member,
                              platform=self.PLATFORM,
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
                           cast_member=cast_member, platform=self.PLATFORM,
                           label=label, update_info=update_info,
                           detail_urls=detail_urls, vids=vids,
                           type=tv_type,
                           detail_titles=detail_titles,
                           detail_episodes=detail_episodes,
                           )
