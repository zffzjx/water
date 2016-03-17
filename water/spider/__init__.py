# coding=utf-8
import requests
import time
from cg_core import utils

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'} # noqa


def request(url, interval=60, cycle_times=3, name='qq'):
    """
    Result for request target url.

    return unicode  type result

    error return None.
    """
    result = requests.get(url, headers=headers)
    while(cycle_times):
        try:
            if result.status_code == 200:
                result.encoding = 'utf8'
                return result.text
            if result.status_code == 500:
                time.sleep(interval)
                utils.log(name, message="网络出现错误,{}秒之后会重新抓取\r\n".format(interval)) # noqa
        except:
            result = None
        cycle_times -= 1
    return result
