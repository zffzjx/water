# coding=utf-8
import os
import datetime
import xlrd


def write(path, name, content):
    fo = open(path + name, 'w')
    fo.write(content)
    fo.close()


def read(path, name):
    try:
        fo = open(path + name, 'r')
        str = fo.read()
        fo.close()
        return str
    except:
        return ""


def mkdir(path):
    is_exists = os.path.exists(path)
    if not is_exists:   # 不存在目录
        os.makedirs(path)


def utc2datetime(t):
    """
    Sends a :class:`float` time value.
    Returns :class:`datetime.datetime` object.

    :param t: :class:`float` time value.
    """
    return datetime.datetime.fromtimestamp(t)


def read_excel(path, name):
    data = xlrd.open_workbook(path + name)
    table = data.sheets()[0]
    ncols = table.ncols
    names = []
    for ncol in xrange(1, ncols):
        for _ in table.col_values(ncol):
            if _ not in [u'电视剧', u'综艺']:
                names.append(_.encode('utf8'))
    return names


def format_seconds(seconds):
    minute = seconds // 60
    second = seconds - minute * 60
    return str(minute) + '分钟' + str(second) + '秒'
