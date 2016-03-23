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
    while(cycle_times):
        try:
            result = requests.get(url, headers=headers)
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
