# coding=utf-8
from spider import request
import re


class Yk(object):

    def tv_urls_map(self):
        tv_urls_map = {}
        urls = ['http://www.youku.com/v_olist/c_97.html',
                'http://www.youku.com/v_olist/c_85.html']
        for url in [urls[0]]:
            for m in re.finditer(u'<div class="p-link">(.|\n)+?</div>',
                                 request(url)):
                url = re.search(u'http.+?\.html', m.group()).group()
                name = re.search(u' title=".+?"', m.group()).group()[8:-1]
                tv_urls_map[name] = url
        return tv_urls_map
