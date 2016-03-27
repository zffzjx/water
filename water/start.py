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
from spider.iqy import Iqy as SpiderIqy
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

    tv_names = tv_names + db_tv_names
    tv_names = list(set(tv_names))

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
    tv_infos = TvInfo.mget_by_platform_and_type(u'iqy', u'电视剧')
    db_tv_names = [_.name for _ in tv_infos]
    for tv_info in tv_infos:
        if not dianshiju_infos.get(tv_info.name) and tv_info.type == u'电视剧':
            dianshiju_infos[tv_info.name] = \
                [
                    {'url': [tv_info.detail_urls]},
                    {'id': tv_info.tv_id},
                    {'v_id': tv_info.vids}]

    iqy_db.dianshiju_info(dianshiju_infos, db_tv_names)

    # zongyi
    zongyi_infos = iqy_spi.zongyi_infos()
    zongyi_infos = {}
    tv_infos = TvInfo.mget_by_platform_and_type(u'iqy', u'综艺')
    db_tv_names = [_.name for _ in tv_infos]
    for tv_info in tv_infos:
        if not zongyi_infos.get(tv_info.name) and tv_info.type == u'综艺':
            zongyi_infos[tv_info.name] = \
                [
                    {'url': tv_info.detail_urls.split(",")},
                    {'id': tv_info.tv_id},
                    {'v_id': tv_info.vids.split(",")}]

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
    Start(start_let, now).start()
    Start(start_sh, now).start()
    Start(start_mg, now).start()
