# coding=utf-8
import re
import json
from spider import request


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
        for m in re.finditer(u'<li  j-delegate="liover"(.|\n)+?</li>',
                             request(zongyi_names_url)):
            url = re.search(u'http.+?html', m.group()).group()
            page = request(url)
            try:
                page = re.search(u'<h2 class="jiemu-tit">.+?</h2>', page).group() # noqa
                name = re.search(u'title=".+?"', page).group()[7:-1]
                url = re.search(u'http.+?\.html', page).group()
            except:
                continue
            if not tv_infos.get(name):
                page = request(url)
                list_id = re.search(u'data-bodansubid="\d+"', page)
                if list_id:
                    url = 'http://cache.video.qiyi.com/jp/plst/{}/?callback=callback' # noqa
                    list_id = re.search(u'\d+', list_id.group()).group()
                    page = request(url.format(list_id.encode('utf8')))
                    json_content = json.loads(re.search(u'\({(.|\n)+}\)', page).group()[1:-1]) # noqa
                    current_number = re.search(u'/\d+/', json_content['data']['plst'][0]['picUrl']).group()[1:-1] # noqa
                    vids = [str(_['tvId']) for _ in json_content['data']['plst']] # noqa
                    description = u''
                    cast_number = u''
                    tv_infos[name] = [vids, current_number, description,
                                      cast_number]
                else:
                    vids = re.finditer(u'<li data-juji-new-tvid="\d+"', page)
                    vids = [str(re.search(u'\d+', _.group()).group()) for
                            _ in vids]
                    if not vids:
                        vids = re.finditer(u'<li data-juji-new-tvid="\d+"', page)
                        vids = [str(re.search(u'\d+', _.group()).group()) for
                    try:
                        current_number = re.search(u'<span class="mod-listTitle_right">.+?</span>', page).group() # noqa
                        current_number = re.compile(u'<.+?>').\
                            sub(u'', current_number)
                    except:
                        continue
                    description = re.search(u'<span class="bigPic-b-jtxt">(.|\n)+?</span>', page) or u''# noqa
                    if description:
                        description = re.compile(u'<.+?>').sub(u'', description.group()) # noqa
                    cast_number = re.search(u'<p class="li-large">主持人：(.|\n)+?</p>', page) or u'' # noqa
                    if cast_number:
                        cast_number = re.compile(u'<.+?>|\s|主持人：'). \
                            sub(u'', cast_number.group())
                    tv_infos[name] = [vids, current_number, description,
                                      cast_number]
            else:
                continue
        return tv_infos
