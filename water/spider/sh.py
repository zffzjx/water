# coding=utf-8
import re
from spider import request


class Sh(object):

    def pids_map(self):
        urls = ['http://tv.sohu.com/hotshow/', 'http://tv.sohu.com/hotdrama/']
        pids_map = {}
        for url in urls:
            page = request(url)
            all_lists = [_.group() for _ in
                         re.finditer(u'<ul class="rList">(.|\n)+?</ul>', page)]
            for all_list in all_lists[:20]:
                for _ in re.finditer(u'<li(.|\n)+?</li>', all_list):
                    pid = re.search(u'data-plid="\d+', _.group())
                    pid = re.search(u'\d+', pid.group()).group()
                    name = re.search(u'title=".+"', _.group()).group()[7:-1]
                    pids_map[name] = pid
        return pids_map
