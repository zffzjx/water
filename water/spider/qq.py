# coding=utf-8
from spider import request
import re
from cg_core import utils
from common import (
    TV_INFO_FILE_DIR,
    PLAY_INFO_FILE_DIR,
    TV_INFO_FILE_FIX,
    PLAY_INFO_FILE_FIX,
)
from common.qq import(
    SAVE_FILE,
    play_info_is_valid_qq,
    tv_info_is_valid_qq
)


class Qq(object):

    def play_info(self, db_tv_infos):
        url = 'http://data.video.qq.com/fcgi-bin/data?tid=70&&appid=10001007&appkey=e075742beb866145&callback=callback&low_login=1&idlist={}&otype=json' # noqa
        play_dir = PLAY_INFO_FILE_DIR + SAVE_FILE
        utils.mkdir(play_dir)
        for tv_info in db_tv_infos:
            if tv_info.type in [u'电视剧']:
                # print u"抓取《{}》播放信息中".format(tv_info.name)
                warning_message = u"Warning《{}》play_info ,结果不准确\r\n". \
                                  format(tv_info.name)
                page = request(url.format(tv_info.tv_id))
                if not play_info_is_valid_qq(page):
                    utils.log(message=warning_message)
                    continue
                utils.write(play_dir, tv_info.name +
                            PLAY_INFO_FILE_FIX, page)
            elif tv_info.type in [u'综艺']:
                vids = tv_info.vids.split(',')
                episodes = tv_info.detail_episodes.split(',')
                for vid, episode in zip(vids, episodes):
                    # print u"抓取《{}》第{}期播放信息中。。。".format(tv_info.name, episode)
                    warning_message = u"Warning《{}》第{}期play_info ,结果不准确\r\n". \
                                      format(tv_info.name, episode)
                    page = request(url.format(vid))
                    if not play_info_is_valid_qq(page):
                        utils.log(message=warning_message)
                        continue
                    utils.write(play_dir, tv_info.name + episode +
                                PLAY_INFO_FILE_FIX, page)
            # print u'play and opinion《{}》抓取完毕'.format(tv_info.name)

    def tv_info(self, tv_names):
        url = 'http://s.video.qq.com/search?comment=1&plat=2&otype=json&query={}&callback=callback'  # noqa
        info_dir = TV_INFO_FILE_DIR + SAVE_FILE
        utils.mkdir(info_dir)
        for name in tv_names:
            warning_message = u"Warning《{}》tv_info ,结果不准确\r\n". \
                              format(name)
            page = request(url.format(name.encode('utf8')))
            if not tv_info_is_valid_qq(page):
                utils.log(message=warning_message)
                continue
            utils.write(info_dir, name + TV_INFO_FILE_FIX,
                        page.encode('utf8'))
            # print u'tv_info/《' + name + u'》抓取完毕'

    def tv_names(self):
        urls = ['http://v.qq.com/rank/detail/2_-1_-1_-1_2_-1.html',
                'http://v.qq.com/rank/detail/10_-1_-1_-1_2_-1.html']
        names = []
        for url in urls:
            result = request(url)
            [names.append(re.compile(u'x_con_item_title"><a.+?>|</a>').
             sub(u'', m.group()))
             for m in re.finditer(u'x_con_item_title"><a.+?</a>', result)]
        return names
