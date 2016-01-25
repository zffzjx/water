# coding=utf-8
from handler.model import (
    PlayInfo,
    TvInfo,
    OpinionInfo,
)
from cg_core import utils
import time
import re
import json
from spider.qq import(
    TV_INFO_FILE_DIR,
    TV_INFO_FILE_FIX,
    TV_INFO_2_FILE_FIX,
    TV_INFO_3_FILE_FIX,
    PLAY_INFO_FILE_DIR,
    PLAY_INFO_FILE_FIX,
    OPINION_INFO_FILE_DIR,
    OPINION_INFO_FILE_FIX,
    OPINION_COMMENT_INFO_FILE_fix,
)


class Qq(object):

    PLATFORM = 'QQ'

    def opinion_info(self, db_tv_ids, db_tv_infos):
        now = utils.utc2datetime(time.time())
        for tv_info in db_tv_infos:
            for vid, title, episode \
                in zip(tv_info.vids.split(','),
                       tv_info.detail_titles.split(','),
                       tv_info.detail_episodes.split(',')):
                if tv_info.type == '电影':
                    vid = tv_info.tv_id
                opinion_str = utils.read(OPINION_INFO_FILE_DIR + tv_info.tv_id + '/', vid + OPINION_INFO_FILE_FIX) # noqa
                opinion_json = json.loads(opinion_str)
                if opinion_json['data']:
                    opinions = opinion_json['data']['subject'][0]['option']
                    like_number = opinions[0]['selected']
                    oppose_number = opinions[1]['selected']
                    comment_str = utils.read(OPINION_INFO_FILE_DIR + tv_info.tv_id + '/', vid + OPINION_COMMENT_INFO_FILE_fix) # noqa
                    comment_json = json.loads(comment_str)
                    comment_number = comment_json['data']['commentnum']
                else:
                    like_number, oppose_number, comment_number = -1, -1, -1
                if vid in db_tv_ids:
                    OpinionInfo.update(
                        v_id=tv_info.tv_id,
                        like_number=like_number,
                        oppose_number=oppose_number,
                        tv_id=vid,
                        time_at=now,
                        comment_number=comment_number,
                        title=title,
                        episode=episode,
                    )
                else:
                    OpinionInfo.add(
                        v_id=tv_info.tv_id,
                        like_number=like_number,
                        oppose_number=oppose_number,
                        tv_id=vid,
                        time_at=now,
                        comment_number=comment_number,
                        title=title,
                        episode=episode,
                    )

    def play_info(self, db_tv_ids, db_tv_infos):
        now = utils.utc2datetime(time.time())
        for tv_info in db_tv_infos:
            if tv_info.type == '综艺':
                for vid in tv_info.vids.split(','):
                    play_info_str = utils.read(PLAY_INFO_FILE_DIR, vid + PLAY_INFO_FILE_FIX) # noqa
                    play_info_json = json.loads(play_info_str)
                    day_play_counts = play_info_json['results'][0]['fields']['tdnumc'] # noqa
                    all_play_counts = play_info_json['results'][0]['fields']['allnumc'] # noqa
                    if vid in db_tv_ids:
                        PlayInfo.update(
                            tv_id=vid,
                            tv_name=tv_info.name,
                            day_play_counts=day_play_counts,
                            all_play_counts=all_play_counts,
                            time_at=now,
                        )
                    else:
                        PlayInfo.add(
                            tv_id=vid,
                            tv_name=tv_info.name,
                            day_play_counts=day_play_counts,
                            all_play_counts=all_play_counts,
                            time_at=now,
                        )
            else:
                play_info_str = utils.read(PLAY_INFO_FILE_DIR, tv_info.tv_id + PLAY_INFO_FILE_FIX) # noqa
                play_info_json = json.loads(play_info_str)
                day_play_counts = play_info_json['results'][0]['fields']['tdnumc'] # noqa
                all_play_counts = play_info_json['results'][0]['fields']['allnumc'] # noqa
                if tv_info.tv_id in db_tv_ids:
                    PlayInfo.update(
                        tv_id=tv_info.tv_id,
                        tv_name=tv_info.name,
                        day_play_counts=day_play_counts,
                        all_play_counts=all_play_counts,
                        time_at=now,
                    )
                else:
                    PlayInfo.add(
                        tv_id=tv_info.tv_id,
                        tv_name=tv_info.name,
                        day_play_counts=day_play_counts,
                        all_play_counts=all_play_counts,
                        time_at=now,
                    )

    def tv_info(self, tv_names, db_tv_names):
        for name in tv_names:
            json_page = utils.read(TV_INFO_FILE_DIR, name + TV_INFO_FILE_FIX)
            json_content = json.loads(json_page)
            play_list = {}
            tv_type = None
            for _ in json_content['list']:
                tv_type = _['BC']
                if tv_type:
                    play_list = _
                    break
            if play_list:
                tv_type = play_list['BC']
                match = re.search('>(.|\n)+?<', tv_type)
                tv_type = match and re.compile('>|<').sub('', match.group()) or tv_type# noqa
                description = play_list['TX']
                last_update_time = play_list['AT']
                update_info = play_list['SS']
                current_number = play_list['TT']
                tv_id = play_list['ID']
                label = play_list['BE']
                cast_member = play_list['BM']
                src_play_list = play_list['src_list']['vsrcarray'][0]['playlist']   # noqa
                if isinstance(src_play_list, dict):
                    src_play_list = src_play_list.values()[0]
                if not src_play_list[0].get('id'):     # not qq platform
                    continue
                if tv_type == u'电视剧':
                    list_url_page = utils.read(TV_INFO_FILE_DIR, name + TV_INFO_3_FILE_FIX) # noqa
                    if list_url_page:
                        list_url_page = json.loads(list_url_page)
                        all_list = list_url_page['video_play_list']['playlist']
                        vids = [_['id'] for _ in all_list]
                        detail_urls = [_['url'] for _ in all_list]
                        vids = ",".join(vids)
                        detail_urls = ",".join(detail_urls)
                        detail_titles = [_['title'] for _ in all_list]
                        detail_titles = ",".join(detail_titles)
                        detail_episodes = [_.get('episode_number') or
                                           _.get('date') for _ in all_list]
                        detail_episodes = ",".join(detail_episodes)
                else:

                    vids = [_['id'] for _ in src_play_list]
                    vids = ",".join(vids)
                    detail_urls = [_['url'] for _ in src_play_list]
                    detail_urls = ",".join(detail_urls)
                    detail_titles = [_['title'] for _ in src_play_list]
                    detail_titles = ",".join(detail_titles)
                    detail_episodes = [_.get('episode_number') or
                                       _.get('date') for _ in src_play_list]
                    detail_episodes = ",".join(detail_episodes)

                html_page = utils.read(TV_INFO_FILE_DIR, name + TV_INFO_2_FILE_FIX) # noqa
                all_number = ''
                if html_page:
                    match = re.search('/共\d+', html_page)
                    all_number = match and re.compile('/共').sub('', match.group()) # noqa
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
