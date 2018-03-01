# -*- coding:utf-8 -*-
import Spider as sp
import Data_Manager as dm
import json

# ↓↓↓↓ 定义top n ↓↓↓↓
topn = 10


# 计算top n主页网站
def calc_topn(json_data):
    topn_urls = {}
    for i in json_data:
        if i['url'] not in topn_urls:
            topn_urls[i['url']] = 1
        else:
            topn_urls[i['url']] += 1

    tops = sorted(topn_urls.iteritems(), key=lambda d: d[1], reverse=True)

    urls = []
    for i in range(0, topn):
        urls.append(tops[i][0])

    for j in range(0, topn):
        print tops[j]
    return urls


# 按24小时统计访问量
def count_day_time(json_data):
    day_time = dict.fromkeys(range(24), 0)

    for i in json_data:
        temp_time = i['lastVisitTime'].split('/')
        clocks = temp_time[3]
        hours = clocks.split(':')
        day_time[int(hours[0])] += i['visitCount']

    return day_time


# 计算星期几
def calc_week(year, month, day):
    if month < 3:
        year -= 1
        month += 12
    c = year/100
    year = year - c * 100
    week = (c / 4) - 2 * c + (year + year / 4) + (13 * (month + 1) / 5) + day - 1  # 蔡勒公式
    if week < 0:
        week += 7
    week %= 7
    return week


# 按星期统计每天访问量
def count_week_time(json_data):
    week_time = {'MON': 0, 'TUE': 0, 'WED': 0, 'THU': 0, 'FRI': 0, 'SAT': 0, 'SUN': 0}
    for i in json_data:
        temp_time = i['lastVisitTime'].split('/')
        year = int(temp_time[0])
        month = int(temp_time[1])
        day = int(temp_time[2])
        week = calc_week(year, month, day)
        visit_times = i['visitCount']
        if week is 1:
            week_time['MON'] += visit_times
        elif week is 2:
            week_time['TUE'] += visit_times
        elif week is 3:
            week_time['WED'] += visit_times
        elif week is 4:
            week_time['THU'] += visit_times
        elif week is 5:
            week_time['FRI'] += visit_times
        elif week is 6:
            week_time['SAT'] += visit_times
        elif week is 0:
            week_time['SUN'] += visit_times
    return week_time


# 按月统计每天访问量
def count_month_time(json_data):
    month_time = dict.fromkeys(range(1, 32), 0)
    for i in json_data:
        temp_time = i['lastVisitTime'].split('/')
        day = int(temp_time[2])
        month_time[day] += i['visitCount']

    return month_time


# 按分类统计
def count_category(json_data):
    form = dm.load_data("files/category_list.json")
    category_count = {'Search': 0, 'Shopping': 0, 'News': 0, 'Entertainment': 0, 'Education': 0, 'Society': 0}
    for i in json_data:
        if form.has_key(i['url']):
            category_count[form[i['url']]] += i['visitCount']
        else:
            category_count['Education'] += i['visitCount']
    return category_count
# dm.transform_data("files/history.json")
# sp.spider(calc_topn(dm.load_data("files/cut_history.json")))

# calc_topn(load_datas())
# count_day_time(dm.load_data("files/cut_history.json"))
# print count_month_time(dm.load_data("files/cut_history.json"))
# print count_category(dm.load_data("files/cut_history.json"))
