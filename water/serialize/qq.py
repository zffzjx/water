# coding=utf-8
import re
from cg_core import utils
from handler.model import (
    PlayInfo,
    TvInfo,
)
from common import (
    TV_INFO_FILE_DIR,
    PLAY_INFO_FILE_DIR,
    TV_INFO_FILE_FIX,
    PLAY_INFO_FILE_FIX
)
from common.qq import(
    PLATFORM,
    SAVE_FILE,
    play_info_is_valid_qq,
    tv_info_is_valid_qq,
    get_playlist,
    get_all_list
)


class Qq(object):

    def __init__(self, now):
        self.now = now

    def play_info(self, db_tv_infos):
        play_dir = PLAY_INFO_FILE_DIR + SAVE_FILE
        for tv_info in db_tv_infos:
            if tv_info.type == u'综艺':
                vids = tv_info.vids.split(',')
                episodes = tv_info.detail_episodes.split(',')
                day_play_counts = 0
                all_play_counts = 0
                for vid, episode in zip(vids, episodes):
                    page = utils.read(play_dir, tv_info.name +
                                      episode + PLAY_INFO_FILE_FIX)
                    json_content = play_info_is_valid_qq(page)
                    if not json_content:
                        continue
                    try:
                        play_infos = json_content['results'][0]['fields']
                        tmp_day_play_counts = play_infos['tdnumc'] or '0'
                        tmp_all_play_counts = play_infos['allnumc'] or '0'
                        all_play_counts += (int)(tmp_all_play_counts)
                        day_play_counts += (int)(tmp_day_play_counts)
                    except:
                        continue
                if self.now.hour < 1:
                    day_play_counts = 0
                PlayInfo.add(
                    tv_id=tv_info.tv_id,
                    tv_name=tv_info.name,
                    day_play_counts=day_play_counts,
                    all_play_counts=all_play_counts,
                    time_at=self.now,
                    platform=PLATFORM,
                    type=u'综艺'
                )
            elif tv_info.type == u'电视剧':
                page = utils.read(play_dir, tv_info.name +
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
                if self.now.hour < 1:
                    day_play_counts = 0
                PlayInfo.add(
                    tv_id=tv_info.tv_id,
                    tv_name=tv_info.name,
                    day_play_counts=day_play_counts,
                    all_play_counts=all_play_counts,
                    time_at=self.now,
                    platform=PLATFORM,
                    type=u'电视剧'
                )

    def tv_info(self, tv_names, db_tv_names):
        info_dir = TV_INFO_FILE_DIR + SAVE_FILE
        for name in tv_names:
            page = utils.read(info_dir, name + TV_INFO_FILE_FIX)
            json_content = tv_info_is_valid_qq(page)
            if not json_content:
                continue
            play_list = get_playlist(json_content)
            tv_type = play_list['BC']
            tv_type = re.search(u'[\u4e00-\u9fa5]+', tv_type).group()
            description = play_list['TX']
            last_update_time = play_list['AT']
            update_info = play_list['SS']
            tv_id = play_list['ID']
            label = play_list['BE']
            cast_member = play_list['BM']
            cast_member = re.compile(u'<.+?>').sub(u'', cast_member)

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
