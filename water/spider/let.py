# coding=utf-8
from spider import request
import re


class Let(object):

    def dianshiju_urls_map(self):
        urls_map = {}
        url = 'http://top.le.com/tvhp.html'
        result = request(url)
        all_lists = re.search(u'<ol class="chart-list j-for"(.|\n)+?</ol>',
                              result)
        all_lists = [_.group() for _ in re.finditer(u'<li>(.|\n)+?</li>',
                     all_lists.group())][1:]
        for lists in all_lists:
            _list = [_.group() for _ in re.finditer(u'<span(.|\n)+?</span>',
                     lists)]
            try:
                name = re.compile(u'<.+?>').sub('', _list[1])
                url = re.search(u'http://.+?\.html', _list[1]).group()
                pid = re.search(u'\d+?\.html', url).group()[:-5]
                cast_member = re.compile(u'<.+?>|\s+').sub(' ', _list[2])
                label = re.compile(u'<.+?>|\s+').sub(' ', _list[4])
            except:
                continue
            urls_map[name] = [url, pid, cast_member, label]
        return urls_map

    def zongyi_urls_map(self):
        urls_map = {}
        url = 'http://top.le.com/varhp.html'
        result = request(url)
        all_lists = re.search(u'<ol class="chart-list j-for"(.|\n)+?</ol>',
                              result)
        all_lists = [_.group() for _ in re.finditer(u'<li>(.|\n)+?</li>',
                     all_lists.group())][1:]
        for lists in all_lists:
            _list = [_.group() for _ in re.finditer(u'<span(.|\n)+?</span>',
                     lists)]
            try:
                name = re.compile(u'<.+?>').sub('', _list[1])
                name = re.search(u'《.+?》', name)
                name = name and name.group()[1:-1] or None
                if not name:
                    continue
                url = re.search(u'http://.+?\.html', _list[1]).group()
                label = re.compile(u'<.+?>|\s+').sub(' ', _list[2])
            except:
                continue
            urls_map[name] = [url, label]
        return urls_map
