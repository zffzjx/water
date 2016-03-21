# coding=utf-8
import re

SAVE_FILE = 'yk/'

PLATFORM = 'yk'


def info_and_play_is_valid(page, name):
    if not page:
        return
    try:
        title_str = re.search(u'<h1 class="title">(.|\n)+?</h1>', page).group()
        _type = re.search(u'target="_blank">.+?<', title_str).group()[16:-1]
        title = re.search(u'class="name">.+?<', title_str).group()[13:-1]
        if _type not in [u'电视剧', u'综艺']:
            return
        if title != name:
            return
        description_str = re. \
            search(u'<span class="short" id="show_info_short"(.|\n)+?</div>',
                   page)
        if not description_str:
            return
    except:
        return
    return page
