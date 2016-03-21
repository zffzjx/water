#!/usr/bin/python
# coding=utf-8
import time
import threading
from serialize.qq import Qq as SerializeQq
from spider.qq import Qq as SpiderQq
from spider.iqy import Iqy as SpiderIqy
from spider.yk import Yk as SpiderYk
from serialize.iqy import Iqy as SerializeIqy
from serialize.yk import Yk as SerializeYk
from handler.model import (
    TvInfo,
    PlayInfo
)
from cg_core import utils

# tv_names = utils.read_excel('../files/', 'names.xlsx')


def start_qq(now):
    start = int(time.time())
    print "qq开始抓取 .."
    qq_spi = SpiderQq()
    qq_db = SerializeQq(now)

    # spider tv_names
    tv_names = qq_spi.tv_names()
    tv_names = list(set(tv_names))

    # spider tv_info
    qq_spi.tv_info(tv_names)

    # db tv_info
    db_tv_names = [_.name for _ in TvInfo.mget_by_platform(u'qq')]
    qq_db.tv_info(tv_names, db_tv_names)

    # spider play
    db_tv_infos = TvInfo.mget_by_platform(u'qq')
    qq_spi.play_info(db_tv_infos)

    # db play_info
    qq_db.play_info(db_tv_infos)

    end = int(time.time())
    print 'qq抓取完毕,耗时', utils.format_seconds(end - start)


def start_iqy(now):
    start = int(time.time())
    print "iqy开始抓取 .."
    iqy_spi = SpiderIqy()
    iqy_db = SerializeIqy(now)

    # dianshiju
    dianshiju_infos = iqy_spi.dianshiju_infos()
    db_tv_names = [_.name for _ in TvInfo.mget_by_platform_and_type(u'iqy',
                   u'电视剧')]
    iqy_db.dianshiju_info(dianshiju_infos, db_tv_names)

    # zongyi
    zongyi_infos = iqy_spi.zongyi_infos()
    db_tv_names = [_.name for _ in TvInfo.mget_by_platform_and_type(u'iqy',
                   u'综艺')]
    iqy_db.zongyi_info(zongyi_infos, db_tv_names)

    # play_info
    db_tv_infos = TvInfo.mget_by_platform(u'iqy')
    db_play_info_map = PlayInfo.mget_map_by_platform_and_time_after(
        'iqy', utils.format_time(time.time(), "%Y-%m-%d"))
    iqy_db.play_info(db_play_info_map, db_tv_infos)
    end = int(time.time())
    print 'iqy抓取完毕,耗时', utils.format_seconds(end - start)


def start_yk(now):
    start = int(time.time())
    print "yk开始抓取 .."
    yk_spi = SpiderYk()
    yk_db = SerializeYk(now)

    # spider urls_map
    tv_urls_map = yk_spi.tv_urls_map()
    # db info and play
    db_tv_names = [_.name for _ in TvInfo.mget_by_platform(u'yk')]
    db_play_info_map = PlayInfo.mget_map_by_platform_and_time_after(
        'yk', utils.format_time(time.time(), "%Y-%m-%d"))
    yk_db.info_and_play(tv_urls_map, db_tv_names, db_play_info_map)
    end = int(time.time())
    print 'yk抓取完毕,耗时', utils.format_seconds(end - start)


class Start(threading.Thread):

    def __init__(self, func, now):
        threading.Thread.__init__(self)
        self.func = func
        self.now = now

    def run(self):
        self.func(self.now)

if __name__ == '__main__':

    now = utils.utc2datetime(time.time())

    Start(start_qq, now).start()
    Start(start_iqy, now).start()
    Start(start_yk, now).start()
