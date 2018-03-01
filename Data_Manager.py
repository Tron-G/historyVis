# -*- coding:utf-8 -*-
from os import path
import json
import datetime
import sys
import operator
import re
reload(sys)
sys.setdefaultencoding('utf-8')


# 加载json文件
# json文件一定是utf8无BOM格式否则报错
def load_data(file_path):#读取数据
    base_path = path.abspath(path.dirname(__file__))
    upload_path = path.join(base_path, file_path)
    f = file(upload_path)
    json_datas = json.load(f)
    return json_datas


def cmp_datetime(a, b):
    a_datetime = datetime.datetime.strptime(a, '%Y/%m/%d/%H:%M:%S')
    b_datetime = datetime.datetime.strptime(b, '%Y/%m/%d/%H:%M:%S')

    if a_datetime > b_datetime:
        return 1
    elif a_datetime < b_datetime:
        return -1
    else:
        return 0


# 数据清洗
def transform_data(file_path):
    json_datas = load_data(file_path)
    for i in json_datas:
        if "PM" in i['lastVisitTime']:
            temp_time = i['lastVisitTime'].split('/')
            clocks = temp_time[3]
            clocks = clocks.replace('PM', '')
            hours = clocks.split(':')
            if (int(hours[0]) + 12) == 24:
                hours[0] = str(0)
            else:
                hours[0] = str(int(hours[0]) + 12)
            temp_time[3] = (':').join(hours).encode("utf8")
            i['lastVisitTime'] = '/'.join(temp_time)

        elif "AM" in i['lastVisitTime']:
            temp_time = i['lastVisitTime'].split('/')
            clocks = temp_time[3]
            clocks = clocks.replace('AM', '')
            temp_time[3] = clocks.encode("utf8")
            i['lastVisitTime'] = '/'.join(temp_time)

    json_datas.sort(cmp=cmp_datetime, key=operator.itemgetter('lastVisitTime'))#按时间排序

    with open("files/full_history.json", 'w') as out_file:
        json.dump(json_datas, out_file, ensure_ascii=False)

    cut_url(json_datas)
    pass


# url提取
def cut_url(json_datas):
    data_url = ''
    new_url = ''
    for i in json_datas:
        data_url = i['url']
        new_url = re.findall(r"http://(.+?)/", data_url)
        if new_url:
            i['url'] = str(new_url[0]).encode("utf8")
        if not new_url:#为空
            new_url = re.findall(r"https://(.+?)/", data_url)
        if new_url:
            i['url'] = str(new_url[0]).encode("utf8")
        if not new_url:
            pass

    with open("files/cut_history.json", 'w') as out_file:
        json.dump(json_datas, out_file, ensure_ascii=False)
    pass


# 按时间提取数据
def change_data(start_time, end_time):

    new_data= []
    json_datas = load_data("files/cut_history.json")
    start = datetime.datetime.strptime(start_time, '%Y/%m/%d')
    end = datetime.datetime.strptime(end_time, '%Y/%m/%d')
    now = ''
    for i in json_datas:
        times = i['lastVisitTime'].split('/')
        now = times[0] + '/' + times[1] + '/' + times[2]
        now_time = datetime.datetime.strptime(now, '%Y/%m/%d')
        if start < now_time < end:
            new_data.append(i)
    # with open("files/tp.json", 'w') as out_file:
    #     json.dump(new_data, out_file, ensure_ascii=False)
    return new_data


# print change_data("2017/12/1", "2017/12/16")