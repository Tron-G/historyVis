# -*- coding:utf-8 -*-
import Spider as sp
import Data_Manager as dm
import math


# 计算top n主页网站 以及饼状图数据
def calc_topn(json_data, is_pie):
    top_n = 10  # 自定义topn
    topn_urls = {}
    title_form = {}
    for i in json_data:
        if i['url'] not in topn_urls:
            topn_urls[i['url']] = i['visitCount']
            title_form[i['url']] = i['title']
        else:
            topn_urls[i['url']] += i['visitCount']
    tops = sorted(topn_urls.iteritems(), key=lambda d: d[1], reverse=True)
    if len(tops) < top_n:
        top_n = len(tops)

    pie_data = []
    spider_data = []
    for i in range(0, top_n):
        temp_data = {'url': tops[i][0], 'count': tops[i][1]}
        sp_data = {'url': tops[i][0], 'title': title_form[tops[i][0]]}
        pie_data.append(temp_data)
        spider_data.append(sp_data)

    if is_pie:
        return pie_data
    else:
        return spider_data


# 条形图数据
def bar_data(json_data):
    day_data = count_day_time(json_data)
    week_data = count_week_time(json_data)
    month_data = count_month_time(json_data)
    bar_json = {'day': day_data, 'week': week_data, 'month': month_data}
    # print json.dumps(bar_json, ensure_ascii=False)
    return bar_json


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


# 按分类统计 雷达图数据
def count_category(json_data):
    form = dm.load_data("files/category_list.json")
    category_count = {'Search': 0, 'Shopping': 0, 'News': 0, 'Entertainment': 0, 'Education': 0, 'Society': 0}
    for i in json_data:
        if form.has_key(i['url']):
            category_count[form[i['url']]] += i['visitCount']
        else:
            category_count['Education'] += i['visitCount']

    total_visit = category_count['Education'] + category_count['Search'] \
                  + category_count['Shopping'] + category_count['Entertainment']\
                  + category_count['Society'] + category_count['News']

    for i in category_count.keys():
        category_count[i] = int(math.ceil(float(category_count[i]*1.0/total_visit)*10))

    radar_data = []
    for j in category_count.keys():
        temp_data = {'area': j, 'value': category_count[j]}
        radar_data.append(temp_data)
    return radar_data


# 词云数据
def words_cloud_data(json_data):
    spider_data = calc_topn(json_data, False)
    count_data = calc_topn(json_data, True)
    # print spider_data,count_data
    words = sp.spider(spider_data)
    # print words
    visit_count = 0
    for i in count_data:
        visit_count += i['count']

    words_list = []
    counter = 0
    for i in words:
        weight = float(count_data[counter]['count']*1.0/visit_count)
        counter += 1
        for key in i.keys():
            temp_word = {'name': key, 'value': i[key] * weight}
            words_list.append(temp_word)

    return words_list


# 饼图比例尺
def pie_data_scale(min_value, max_value, num):
    add_num = float((num - min_value)*1.0/(max_value - min_value)*65)
    trans_num = float(5.0 + add_num)
    return trans_num


# 分段时间饼图数据
def feature_pie_data(json_data):
    day_section = []
    category_names = ['midnight', 'morning', 'noon', 'afternoon', 'evening', 'night']
    section_visit_count = [0]*6
    day_time = count_day_time(json_data)

    for i in range(0, 23):
        if 0 <= i < 7:
            section_visit_count[0] += day_time[i]
        elif 7 <= i < 11:
            section_visit_count[1] += day_time[i]
        elif 11 <= i < 14:
            section_visit_count[2] += day_time[i]
        elif 14 <= i < 17:
            section_visit_count[3] += day_time[i]
        elif 17 <= i < 19:
            section_visit_count[4] += day_time[i]
        elif 19 <= i <= 23:
            section_visit_count[5] += day_time[i]

    for j in range(0, 6):
        temp_section = {}
        temp_section['section'] = category_names[j]
        temp_section['visit_count'] = section_visit_count[j]
        temp_section['scale'] = pie_data_scale(min(section_visit_count), max(section_visit_count), section_visit_count[j])
        temp_section['sort'] = j
        day_section.append(temp_section)

    return day_section


# words_cloud_data(dm.load_data("files/cut_history.json"))
# print json.dumps(calc_topn(dm.load_data("files/cut_history.json")), ensure_ascii=False)
