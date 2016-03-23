# coding=utf-8
import re
from spider import request
from common.mg import TV_TYPE_MAP


class Mg(object):

    def pids_map(self):
        urls = ['http://www.mgtv.com/tv/rbjj/',
                'http://www.mgtv.com/show/wprb/']
        pids_map = {}
        lists = []
        for url in [urls[1]]:
            page = request(url)
            all_lists = re.search(u'<ul class="clearfix ullist-ele">(.|\n)+?</ul>', page).group() # noqa
            for _list in re.finditer(u' <li>(.|\n)+?</li>', all_lists):
                name = re.search(u'<span class="a-pic-t1".+?</span>',
                                 _list.group()).group()
                name = re.compile(u'<.+?>').sub(u'', name)
                try:
                    pid = re.search(u'/\d+?/f', _list.group()).group()[1:-2]
                    type_n = (int)(re.search(u'v/\d+?/', _list.group()).group()[2:-1]) # noqa
                except:
                    continue
                if type_n not in TV_TYPE_MAP.keys():
                    continue
                if pid not in lists:
                    lists.append(pid)
                    pids_map[name] = [pid, type_n]
        return pids_map
