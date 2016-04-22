# coding=utf-8
import requests
import time
import re
from cg_core import utils

name_map = {
    u'一': u'1',
    u'二': u'2',
    u'三': u'3',
    u'四': u'4',
    u'五': u'5',
    u'六': u'6',
    u'七': u'7',
    u'八': u'8',
    u'九': u'9',
}

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'} # noqa


def request(url, interval=60, cycle_times=3, name='qq', headers={}):
    """
    Result for request target url.

    return unicode  type result

    error return None.
    """
    while(cycle_times):
        try:
            result = requests.get(url, headers=headers, timeout=3)
            if result.status_code == 200:
                if result.encoding and result.encoding.lower() == 'gbk':
                    text = result.text
                    text = text.encode('utf8')
                    text = text.decode('utf8')
                    return text
                result.encoding = 'utf8'
                return result.text
            if result.status_code == 500:
                time.sleep(interval)
                utils.log(message="网络出现错误,{}秒之后会重新抓取\r\n".format(interval)) # noqa
        except:
            result = None
        cycle_times -= 1
    return result


def convert_name(name):
    def convert_number(number):
        if number == u'十':
            return '10'
        tmp = int(''.join([name_map.get(_) if name_map.get(_) is not None else
                  _ for _ in number]))
        if number[-1] == u'十':
            tmp *= 10
        if number[-1] == u'百':
            tmp *= 100
        if number[-1] == u'千':
            tmp *= 1000
        if number[0] == u'十':
            tmp += 10

        return (str(tmp)).decode('utf8')

    fix = re.search(u'第.+季', name)
    if fix:
        fix = fix.group()
        if fix in name:
            name = re.compile(u'第.+季').sub(u'第' + convert_number(fix[1:-1]) +  u'季', name) # noqa
    return name.replace(u" ", u"")
