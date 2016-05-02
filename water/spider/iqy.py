# coding=utf-8
import re
import json
import random
from spider import request


class Iqy(object):

    def dianshiju_infos(self):
        tv_infos = {}
        dianshi_names_url = 'http://top.iqiyi.com/dianshiju.html?rdm=' + \
            str(random.randint(1, 100000))
        for m in re.finditer(u' <li  j-delegate="liover"(.|\n)+?</li>',
                             request(dianshi_names_url)):
            name = re.search(u'title=".+?"', m.group()).group()[7:-1]
            print name
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
        zongyi_names_url = 'http://top.iqiyi.com/index/top50.htm?cid=6&dim=day' + str(random.randint(1, 100000)) # noqa
        list_url = 'http://cache.video.qiyi.com/jp/sdvlst/6/{}/?callback=callback' # noqa
        for m in re.finditer(u'<li  j-delegate="liover"(.|\n)+?</li>',
                             request(zongyi_names_url)):
            url = re.search(u'http.+?html', m.group()).group()
            page = request(url)
            try:
                head = re.search(u'<h2 class="jiemu-tit">.+?</h2>', page).group() # noqa
                name = re.search(u'title=".+?"', head).group()[7:-1]
                url = re.search(u'http.+?\.html', head).group()
                id = re.search(u'sourceId:\d+', page)
                if not id:
                    continue
                id = re.search(u'\d+', id.group()).group()
            except:
                continue
            if not tv_infos.get(name):
                page = request(url)
                description = re.search(u'<span class="bigPic-b-jtxt">(.|\n)+?</span>', page) or u''# noqa
                if description:
                    description = re.compile(u'<.+?>').sub(u'', description.group()) # noqa
                cast_member = re.search(u'<p class="li-large">主持人：(.|\n)+?</p>', page) or u'' # noqa
                if cast_member:
                    cast_member = re.compile(u'<.+?>|\s|主持人：'). \
                        sub(u'', cast_member.group())

                lists = request(list_url.format(id.encode('utf8')))
                try:
                    lists = re.search(u'\({(.|\n)*}\)', lists).group()[1:-1]
                    json_lists = json.loads(lists)
                    vids = [str(_.get('tvId')) for _ in json_lists.get('data')]
                    current_number = json_lists.get('data')[0]['tvYear']
                except:
                    continue
                tv_infos[name] = [vids, current_number, description,
                                  cast_member]
            else:
                continue
        return tv_infos
