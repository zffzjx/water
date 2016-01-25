# coding=utf-8
# from spider.qq import Qq
from serialize.qq import Qq as SerializeQq
from spider.qq import Qq as SpiderQq
from handler.model import (
    TvInfo,
    PlayInfo,
    OpinionInfo,
)
from cg_core import utils
import time

tv_names = utils.read_excel('../files/', 'names.xlsx')

if __name__ == '__main__':
    start = int(time.time())
    print "开始抓取 .."
    #   spider tv_info
    # SpiderQq().tv_info(tv_names)

    #   db tv_info
    db_tv_infos = TvInfo.mget()
    db_tv_names = [_.name for _ in db_tv_infos]
    SerializeQq().tv_info(tv_names, db_tv_names)

    #   spider play and opinion info
    # db_tv_infos = TvInfo.mget()
    # SpiderQq().play_info(db_tv_infos)

    # db play_info
    db_tv_ids = [_.tv_id for _ in PlayInfo.mget()]
    SerializeQq().play_info(db_tv_ids, db_tv_infos)

    # db opinion info
    db_tv_ids = [_.tv_id for _ in OpinionInfo.mget()]
    SerializeQq().opinion_info(db_tv_ids, db_tv_infos)
    end = int(time.time())
    print '抓取完毕,耗时', utils.format_seconds(end - start)
