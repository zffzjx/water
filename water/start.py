#!/usr/bin/python
# coding=utf-8
import time
import threading
from handler.model import (
    TvInfo,
    PlayInfo
)
from cg_core import utils

from spider.qq import Qq as SpiderQq
# from spider.iqy import Iqy as SpiderIqy
from spider.yk import Yk as SpiderYk
from spider.let import Let as SpiderLet
from spider.sh import Sh as SpiderSh
from spider.mg import Mg as SpiderMg

from serialize.qq import Qq as SerializeQq
from serialize.iqy import Iqy as SerializeIqy
from serialize.yk import Yk as SerializeYk
from serialize.let import Let as SerializeLet
from serialize.sh import Sh as SerializeSh
from serialize.mg import Mg as SerializeMg

from common.mg import TV_TYPE_MAP

# tv_names = utils.read_excel('../files/', 'names.xlsx')


def start_qq(now, names):
    start = int(time.time())
    print "qq开始抓取 .."
    qq_spi = SpiderQq()
    qq_db = SerializeQq(now)

    # spider tv_info
    qq_spi.tv_info(names)

    # db tv_info
    db_tv_names = [_.name for _ in TvInfo.mget_by_platform(u'qq')]
    qq_db.tv_info(names, db_tv_names)

    tv_names = names + db_tv_names
    tv_names = list(set(tv_names))

    # spider play
    db_tv_infos = TvInfo.mget_by_platform(u'qq')
    qq_spi.play_info(db_tv_infos)

    # db play_info
    qq_db.play_info(db_tv_infos)

    end = int(time.time())
    print 'qq抓取完毕,耗时', utils.format_seconds(end - start)


def start_iqy(now, names):
    start = int(time.time())
    print "iqy开始抓取 .."

    db_tv_ids = [int(_.tv_id) for _ in TvInfo.mget_by_platform(u'iqy')]
    iqy = SerializeIqy(now)
    iqy.info_and_play(names, db_tv_ids)
    db_play_info_map = PlayInfo.mget_map_by_platform_and_time_after(
        'iqy', utils.format_time(time.time(), "%Y-%m-%d"))
    db_tv_infos = TvInfo.mget_by_platform(u'iqy')
    iqy.play_info(db_play_info_map, db_tv_infos)
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
    tv_infos = TvInfo.mget_by_platform(u'yk')
    db_tv_names = [_.name for _ in tv_infos]

    db_play_info_map = PlayInfo.mget_map_by_platform_and_time_after(
        'yk', utils.format_time(time.time(), "%Y-%m-%d"))
    for tv_info in tv_infos:
        if not tv_urls_map.get(tv_info.name):
            tv_urls_map[tv_info.name] = tv_info.detail_urls
    yk_db.info_and_play(tv_urls_map, db_tv_names, db_play_info_map)
    end = int(time.time())
    print 'yk抓取完毕,耗时', utils.format_seconds(end - start)


def start_let(now):
    start = int(time.time())
    print "let开始抓取 .."
    let_spi = SpiderLet()
    let_db = SerializeLet(now)

    # dianshiju
    dianshiju_urls_map = let_spi.dianshiju_urls_map()
    tv_infos = TvInfo.mget_by_platform(u'let')
    db_tv_names = [_.name for _ in tv_infos]

    db_play_info_map = PlayInfo.mget_map_by_platform_and_time_after(
        'let', utils.format_time(time.time(), "%Y-%m-%d"))
    for tv_info in tv_infos:
        if not dianshiju_urls_map.get(tv_info.name) and tv_info.type == u'电视剧': # noqa
            dianshiju_urls_map[tv_info.name] = [tv_info.detail_urls, tv_info.tv_id, tv_info.cast_member, tv_info.label] # noqa

    let_db.dianshiju(dianshiju_urls_map, db_tv_names, db_play_info_map)
    # zongyi
    zongyi_urls_map = let_spi.zongyi_urls_map()
    for tv_info in tv_infos:
        if not zongyi_urls_map.get(tv_info.name) and tv_info.type == u'综艺':
            zongyi_urls_map[tv_info.name] = [tv_info.detail_urls, tv_info.label] # noqa

    let_db.zongyi(zongyi_urls_map, db_tv_names, db_play_info_map)
    end = int(time.time())
    print 'let抓取完毕,耗时', utils.format_seconds(end - start)


def start_sh(now):
    start = int(time.time())
    print "sh开始抓取 .."
    sh_spi = SpiderSh()
    sh_db = SerializeSh(now)
    # db
    pids_map = sh_spi.pids_map()
    tv_infos = TvInfo.mget_by_platform(u'sh')
    db_tv_names = [_.name for _ in tv_infos]
    for tv_info in tv_infos:
        if not pids_map.get(tv_info.name):
            pids_map[tv_info.name] = tv_info.tv_id
    db_play_info_map = PlayInfo.mget_map_by_platform_and_time_after(
        'sh', utils.format_time(time.time(), "%Y-%m-%d"))
    sh_db.info_and_play(pids_map, db_tv_names, db_play_info_map)

    end = int(time.time())
    print 'sh抓取完毕,耗时', utils.format_seconds(end - start)


def start_mg(now):
    start = int(time.time())
    print "mg开始抓取 .."
    mg_spi = SpiderMg()
    mg_db = SerializeMg(now)
    # db
    pids_map = mg_spi.pids_map()
    tv_infos = TvInfo.mget_by_platform(u'mg')
    db_tv_names = [_.name for _ in tv_infos]
    reverse = {v: k for k, v in TV_TYPE_MAP.iteritems()}
    for tv_info in tv_infos:
        if not pids_map.get(tv_info.name):
            type_n = reverse[tv_info.type]
            print 'type_n=', type_n
            pids_map[tv_info.name] = [tv_info.tv_id, type_n]

    db_play_info_map = PlayInfo.mget_map_by_platform_and_time_after(
        'mg', utils.format_time(time.time(), "%Y-%m-%d"))
    mg_db.info_and_play(pids_map, db_tv_names, db_play_info_map)
    end = int(time.time())
    print 'mg抓取完毕,耗时', utils.format_seconds(end - start)


class Start(threading.Thread):

    def __init__(self, func, now, names):
        threading.Thread.__init__(self)
        self.func = func
        self.now = now
        self.names = names

    def run(self):
        self.func(self.now, self.names)

if __name__ == '__main__':

    now = utils.utc2datetime(time.time())

    qq_spi = SpiderQq()
    iqy = SerializeIqy(now)

    spider_names = qq_spi.tv_names() + iqy.get_names()

    db_names = [_.name for _ in TvInfo.mget()]

    names = list(set(spider_names + db_names))

    # names = [u'爱情公寓4', u'奔跑吧兄弟第三季']
    Start(start_iqy, now, names).start()
    Start(start_qq, now, names).start()
    # Start(start_yk, now).start()
    # Start(start_let, now).start()
    # Start(start_sh, now).start()
    # Start(start_mg, now).start()
