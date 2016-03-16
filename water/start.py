# coding=utf-8
from serialize.qq import Qq as SerializeQq
from spider.qq import Qq as SpiderQq
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
        print "QQ开始抓取 .."
        qq_spi = SpiderQq()
        qq_db = SerializeQq(now)

        # spider tv_names
        tv_names = qq_spi.tv_names()
        tv_names = list(set(tv_names))

        # spider tv_info
        qq_spi.tv_info(tv_names)

        # db tv_info
        db_tv_names = [_.name for _ in TvInfo.mget()]
        qq_db.tv_info(tv_names, db_tv_names)

        # spider play
        db_tv_infos = TvInfo.mget()
        qq_spi.play_info(db_tv_infos)

        # db play_info
        qq_db.play_info(db_tv_infos)

        end = int(time.time())
        print 'QQ抓取完毕,耗时', utils.format_seconds(end - start)

    start_qq()
