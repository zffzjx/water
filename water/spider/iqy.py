# coding=utf-8
from spider import request
import re


class Iqy(object):

    def dianshiju_infos(self):
        tv_infos = {}
        dianshi_names_url = 'http://top.iqiyi.com/dianshiju.html'
        for m in re.finditer(u' <li  j-delegate="liover"(.|\n)+?</li>',
                             request(dianshi_names_url)):
            name = re.search(u'title=".+?"', m.group()).group()[7:-1]
            url = re.search(u'http.+?html', m.group()).group()
            x_id_str = request(url)
            id = re.search(u'data-player-tvid=".+?"', x_id_str).group()[18:-1]
            v_id = re.search(u'data-player-videoid=".+?"', x_id_str). \
                group()[21:-1]
            tv_infos[name] = [{'url': url}]
            tv_infos[name].append({'id': id})
            tv_infos[name].append({'v_id': v_id})
        return tv_infos

    def zongyi_infos(self):
        tv_infos = {}
        zongyi_names_url = 'http://top.iqiyi.com/index/top50.htm?cid=6&dim=day'
        for m in re.finditer(u' <li  j-delegate="liover"(.|\n)+?</li>',
                             request(zongyi_names_url)):
            name = re.search(u'title=".+?"', m.group()).group()[7:-1]
            name = re.search(u'.+?之', name).group()[:-1]
            url = re.search(u'http.+?html', m.group()).group()
            x_id_str = request(url)
            id = re.search(u'data-player-tvid=".+?"', x_id_str).group()[18:-1]
            v_id = re.search(u'data-player-videoid=".+?"', x_id_str). \
                group()[21:-1]
            if not tv_infos.get(name):
                tv_infos[name] = [{'url': [url]}]
                tv_infos[name].append({'id': [id]})
                tv_infos[name].append({'v_id': [v_id]})
            else:
                tv_infos[name][0]['url'].append(url)
                tv_infos[name][1]['id'].append(id)
                tv_infos[name][2]['v_id'].append(v_id)
        return tv_infos
