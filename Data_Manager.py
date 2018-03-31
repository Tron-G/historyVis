# -*- coding:utf-8 -*-
from os import path
import json
import datetime
import sys
import operator
import re
reload(sys)
sys.setdefaultencoding('utf-8')


# 缓存时间范围
def save_cache(data):
    filepath = 'files/cache.json'
    base_path = path.abspath(path.dirname(__file__))
    upload_path = path.join(base_path, filepath)
    with open(upload_path, 'w') as load_f:
        print data
        json.dump(data, load_f, ensure_ascii=False)
    pass


# 加载json文件
# json文件一定是utf8无BOM格式否则报错
def load_data(file_path):  # 读取数据
    base_path = path.abspath(path.dirname(__file__))
    upload_path = path.join(base_path, file_path)
    f = file(upload_path)
    json_datas = json.load(f)
    return json_datas


# 保存json文件
def save_json_data(json_data, file_path):
    base_path = path.abspath(path.dirname(__file__))
    upload_path = path.join(base_path, file_path)

    with open(upload_path, 'w') as out_file:
        json.dump(json_data, out_file, ensure_ascii=False)
    pass


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

    save_json_data(json_datas, "files/full_history.json")

    cut_url(json_datas)
    cut_time(json_datas)
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
        if not new_url:  # 为空
            new_url = re.findall(r"https://(.+?)/", data_url)
        if new_url:
            i['url'] = str(new_url[0]).encode("utf8")
        if not new_url:
            pass

    save_json_data(json_datas, "files/cut_history.json")
    pass


# 时间轴数据计算
def cut_time(json_data):
    axis_json = []
    is_equal = False
    data_len = len(json_data)-1
    for i in range(0, data_len):
        if not is_equal:
            temp_data = {'visitCount': 0}

        times = json_data[i]['lastVisitTime'].split('/')
        now = times[0] + '/' + times[1] + '/' + times[2]
        temp_data['lastVisitTime'] = now
        temp_data['visitCount'] += json_data[i]['visitCount']
        last_time = datetime.datetime.strptime(now, '%Y/%m/%d')

        next_info = json_data[i+1]['lastVisitTime'].split('/')
        next = next_info[0] + '/' + next_info[1] + '/' + next_info[2]
        next_time = datetime.datetime.strptime(next, '%Y/%m/%d')

        if next_time != last_time:
            is_equal = False
            axis_json.append(temp_data)

            if i == data_len-1:
                temp_data = {'lastVisitTime': next, 'visitCount': json_data[i + 1]['visitCount']}
                axis_json.append(temp_data)

        elif next_time == last_time:
            is_equal = True
            if i == data_len-1:
                temp_data['visitCount'] += json_data[i+1]['visitCount']
                axis_json.append(temp_data)

    # print json.dumps(axis_json, ensure_ascii=False)
    save_json_data(axis_json, "files/time_cut_history.json")
    pass


# 按时间提取数据
def change_data(select_data, is_spider):
    start_time = select_data['beginTime']
    end_time = select_data['endTime']
    # print start_time,end_time
    new_data = []
    if is_spider:
        json_datas = load_data("files/full_history.json")
    else:
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
    return new_data




# transform_data("files/history.json")