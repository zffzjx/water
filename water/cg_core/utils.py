# coding=utf-8
import os
import datetime
import xlrd
import time


def write(path, name, content, access_mode='w'):
    fo = open(path + name, access_mode)
    if isinstance(content, unicode):
        content = content.encode('utf8')
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
    return datetime.datetime.fromtimestamp(t)


def datetime2utc(dt):
    return time.mktime(dt.timetuple())


def format_time(t, format_str="%Y-%m-%d %H:%M:%S"):
    return time.strftime(format_str, time.localtime(t))


def read_excel(path, name):

    data = xlrd.open_workbook(path + name)
    # ncols = table.ncols
    names = []
    for sheet in [0, 1]:
        table = data.sheets()[sheet]
        for _ in table.col_values(1):
            if _ not in [u'电视剧', u'综艺']:
                names.append(_.encode('utf8'))
    return names


def format_seconds(seconds):
    minute = seconds // 60
    second = seconds - minute * 60
    return str(minute) + '分钟' + str(second) + '秒'


def log(path='../logs/', name='', message='', level='Warning'):
    mkdir(path)
    write(path, level, format_time(time.time()) + message, 'a')
