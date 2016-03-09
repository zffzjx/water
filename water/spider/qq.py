# coding=utf-8
import requests
from cg_core import utils
import re
import json

TV_INFO_FILE_DIR = '../files/tv_info/'
PLAY_INFO_FILE_DIR = '../files/play_info/'
OPINION_INFO_FILE_DIR = '../files/opinion_info/'

TV_INFO_FILE_FIX = '.json'
TV_INFO_2_FILE_FIX = '.html'
TV_INFO_3_FILE_FIX = '.list'
PLAY_INFO_FILE_FIX = '.json'

OPINION_INFO_FILE_FIX = '.json'
OPINION_COMMENT_INFO_FILE_fix = '.cmt'

REG_FOR_JSON = '{(.|\n)*\}'

LOGS_DIR = '../logs/'
WARNING_FILE = 'spider_warning.log'


class Qq(object):

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'} # noqa

    def play_info(self, db_tv_infos):
        url_get_comment_id = 'http://ncgi.video.qq.com/fcgi-bin/video_comment_id?otype=json&callback=jQuery191006832736660726368_1453219643557&low_login=1&op=3&{}={}&_=1453219643560' # noqa
        url_get_opinion = 'http://coral.qq.com/article/{}/voteinfo?logintype=0&callback=jQuery111105170982657000422_1453219646497&_=1453219646498' # noqa
        url_get_comment_number = 'http://coral.qq.com/article/{}/commentnum?callback=jQuery1910727976780384779_1453256883226&low_login=1&_=1453256883243' # noqa
        url_get_play_number = 'http://data.video.qq.com/fcgi-bin/data?tid=70&&appid=10001007&appkey=e075742beb866145&callback=jQuery19104518115830142051_1453220709669&low_login=1&idlist={}&otype=json&_=1453220709671' # noqa
        for tv_info in db_tv_infos:
            vids = tv_info.vids.split(',')
            play_info_path = PLAY_INFO_FILE_DIR
            opinion_info_path = OPINION_INFO_FILE_DIR + tv_info.tv_id + '/'
            utils.mkdir(opinion_info_path)
            utils.mkdir(play_info_path)
            for vid in vids:
                print u"抓取《{}》第{}集播放信息中。。。".format(tv_info.name, vid)
                if tv_info.type == u'电影':
                    vid = tv_info.tv_id
                try:
                    comment_id_str = requests.get(url_get_comment_id.format('vid', vid), headers=self.headers)    # noqa
                except:
                    utils.write(LOGS_DIR, WARNING_FILE, "Warning tv_info/《"+ name + "》网络错误\r\n", 'a') # noqa
                    continue
                comment_id_str.encoding = 'utf8'
                comment_id_json = re.search(REG_FOR_JSON, comment_id_str.text).group().encode('utf8')    # noqa
                comment_id_json = json.loads(comment_id_json)
                comment_id = comment_id_json.get('comment_id')
                if not comment_id:
                    try:
                        comment_id_str = requests.get(url_get_comment_id.format('cid', vid), headers=self.headers)   # noqa
                    except:
                        utils.write(LOGS_DIR, WARNING_FILE, "Warning tv_info/《"+ name + "》网络错误\r\n", 'a') # noqa
                        continue
                    comment_id_str.encoding = 'utf8'
                    comment_id_json = re.search(REG_FOR_JSON, comment_id_str.text).group().encode('utf8')    # noqa
                    comment_id_json = json.loads(comment_id_json)
                    comment_id = comment_id_json.get('comment_id')
                try:
                    opinion_str = requests.get(url_get_opinion.format(comment_id), headers=self.headers)    # noqa
                except:
                    utils.write(LOGS_DIR, WARNING_FILE, "Warning tv_info/《"+ name + "》网络错误\r\n", 'a') # noqa
                    continue
                opinion_str.encoding = 'utf8'
                opinion_json = re.search(REG_FOR_JSON, opinion_str.text).group().encode('utf8')    # noqa
                utils.write(opinion_info_path, vid + OPINION_INFO_FILE_FIX, opinion_json)    # noqa

                try:
                    comment_str = requests.get(url_get_comment_number.format(comment_id), headers=self.headers)    # noqa
                except:
                    utils.write(LOGS_DIR, WARNING_FILE, "Warning tv_info/《"+ name + "》网络错误\r\n", 'a') # noqa
                    continue
                comment_str.encoding = 'utf8'
                comment_json = re.search(REG_FOR_JSON, comment_str.text).group().encode('utf8')    # noqa
                utils.write(opinion_info_path, vid + OPINION_COMMENT_INFO_FILE_fix, comment_json)    # noqa
                if tv_info.type == u'综艺':
                    print u"抓取《{}》第{}集播放信息中。。。".format(tv_info.name, vid)
                    try:
                        play_number_str = requests.get(url_get_play_number.format(vid), headers=self.headers)    # noqa
                    except:
                        utils.write(LOGS_DIR, WARNING_FILE, "Warning tv_info/《"+ name + "》网络错误\r\n", 'a') # noqa
                        continue
                    play_number_str.encoding = 'utf8'
                    play_number_json = re.search(REG_FOR_JSON, play_number_str.text).group().encode('utf8')    # noqa
                    utils.write(play_info_path, vid + PLAY_INFO_FILE_FIX, play_number_json) # noqa

            if tv_info.type in [u'电视剧', u'电影']:
                print u"抓取《{}》第{}集播放信息中。。。".format(tv_info.name, vid)
                try:
                    play_number_str = requests.get(url_get_play_number.format(tv_info.tv_id), headers=self.headers)    # noqa
                except:
                    utils.write(LOGS_DIR, WARNING_FILE, "Warning tv_info/《"+ name + "》网络错误\r\n", 'a') # noqa
                    continue
                play_number_str.encoding = 'utf8'
                play_number_json = re.search(REG_FOR_JSON, play_number_str.text).group().encode('utf8')    # noqa
                utils.write(play_info_path, tv_info.tv_id + PLAY_INFO_FILE_FIX, play_number_json) # noqa
            print u'play and opinion《{}》抓取完毕'.format(tv_info.name)

    def tv_info(self, tv_names):
        url_json = 'http://s.video.qq.com/search?comment=1&stype=0&plat=2&otype=json&query={}&pver=0&tabid=0&sort=0&cur=0&num=0&start=0&end=20&stag=txt.historyword&referrer=http%3A%2F%2Fv.qq.com%2F&preqid=OXV_5wng6XCqvRKetkWpyxp1Ldmf7jViwrJsmKrAxvjrkrLhmxjSAg&rsrc=0&pltimefilter=0&ndh=&pubtime=0&cgi=search&plver=1&qc=1&qc_version=1&callback=jQuery191047629237337969244_1453169176931&_=1453169176932'  # noqa
        all_list = 'http://s.video.qq.com/loadplaylist?callback=jQuery19108033160881604999_1453307625794&low_login=1&type=4&id={}&plname=qq&vtype=2&video_type=2&inorder=1&otype=json&start=1&end={}&_=1453307625797' # noqa
        for name in tv_names:
            print 'tv_info/《' + name + '》开始抓取'
            try:
                page = requests.get(url_json.format(name), headers=self.headers) # noqa
            except:
                utils.write(LOGS_DIR, WARNING_FILE, "Warning tv_info/《"+ name + "》网络错误\r\n", 'a') # noqa
                continue
            page.encoding = 'utf8'
            json_content = re.search(REG_FOR_JSON, page.text).group().encode('utf8')    # noqa
            utils.mkdir(TV_INFO_FILE_DIR)
            utils.write(TV_INFO_FILE_DIR, name + TV_INFO_FILE_FIX, json_content)    # noqa
            try:
                json_content = json.loads(json_content)
            except:
                continue
            play_list = {}
            tv_type = None
            if not json_content.get('list'):
                utils.write(LOGS_DIR, WARNING_FILE, "Warning tv_info/《"+ name + "》抓取完毕,但是结果为空\r\n", 'a') # noqa
                continue
            for _ in json_content['list']:
                tv_type = _['BC']
                if tv_type:
                    play_list = _
                    break
            if play_list:
                tv_id = play_list['ID']
                try:
                    src_play_list = play_list['src_list']['vsrcarray'][0].get('playlist') # noqa
                except:
                    utils.write(LOGS_DIR, WARNING_FILE, "Warning tv_info/《"+ name + "》抓取完毕,但是结果为空\r\n", 'a') # noqa
                    continue
                if not src_play_list:
                    utils.write(LOGS_DIR, WARNING_FILE, "Warning tv_info/《"+ name + "》抓取完毕,但是结果为空\r\n", 'a') # noqa
                    continue
                if isinstance(src_play_list, dict):
                    src_play_list = src_play_list.values()[0]
                if not src_play_list[0].get('id'):     # not qq platform
                    utils.write(LOGS_DIR, WARNING_FILE, "Warning tv_info/《"+ name + "》不是在QQ平台播放\r\n", 'a') # noqa
                    continue
                last_number = src_play_list[-1]['episode_number']
                if tv_type == u'电视剧':
                    try:
                        all_play_list_str = requests.get(all_list.format(tv_id, last_number))   # noqa
                    except:
                        utils.write(LOGS_DIR, WARNING_FILE, "Warning tv_info/《"+ name + "》网络错误\r\n", 'a') # noqa
                        continue
                    all_play_list_str.encoding = 'utf8'
                    all_play_list = re.search(REG_FOR_JSON, all_play_list_str.text).group().encode('utf8')    # noqa
                    utils.write(TV_INFO_FILE_DIR, name + TV_INFO_3_FILE_FIX, all_play_list)    # noqa

                play_url = str(src_play_list[0]['url'])
                try:
                    page = requests.get(play_url, headers=self.headers)
                except:
                    utils.write(LOGS_DIR, WARNING_FILE, "Warning tv_info/《"+ name + "》网络错误\r\n", 'a') # noqa
                    continue
                page.encoding = 'utf8'
                html_conrtent = page.text.encode('utf8')
                utils.write(TV_INFO_FILE_DIR, name + TV_INFO_2_FILE_FIX, html_conrtent)    # noqa

            print 'tv_info/《' + name + '》抓取完毕'
