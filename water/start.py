# coding=utf-8
from serialize.qq import Qq as SerializeQq
from spider.qq import Qq as SpiderQq
from spider.iqy import Iqy as SpiderIqy
from serialize.iqy import Iqy as SerializeIqy
from handler.model import (
    TvInfo
)
from cg_core import utils
import time

# tv_names = utils.read_excel('../files/', 'names.xlsx')

if __name__ == '__main__':
    now = utils.utc2datetime(time.time())

    def start_qq():
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

    def start_iqy():
        start = int(time.time())
        print "iqy开始抓取 .."
        iqy_spi = SpiderIqy()
        iqy_db = SerializeIqy()
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
        end = int(time.time())
        print 'iqy抓取完毕,耗时', utils.format_seconds(end - start)

    # start_qq()
    start_iqy()
