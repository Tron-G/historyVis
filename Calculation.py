# -*- coding:utf-8 -*-
import random
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
    c = year / 100
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
        temp_url = i['url']
        if 'www.' in temp_url:
            temp_url = temp_url.replace('www.', '')
        if form.has_key(temp_url):
            category_count[form[temp_url]] += i['visitCount']
        else:
            category_count['Education'] += i['visitCount']

    total_visit = category_count['Education'] + category_count['Search'] \
                  + category_count['Shopping'] + category_count['Entertainment'] \
                  + category_count['Society'] + category_count['News']

    for i in category_count.keys():
        category_count[i] = int(math.ceil(float(category_count[i] * 1.0 / total_visit) * 10))

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
        weight = float(count_data[counter]['count'] * 1.0 / visit_count)
        counter += 1
        for key in i.keys():
            temp_word = {'name': key, 'value': i[key] * weight}
            words_list.append(temp_word)

    dm.save_json_data(words_list, 'files/words.json')
    # return words_list


# 比例尺
def pie_data_scale(min_value, max_value, min_target, max_target, num, is_int):
    add_num = float((num - min_value) * 1.0 / (max_value - min_value) * (max_target - min_target))
    trans_num = float(min_target + add_num)
    if is_int:
        return round(trans_num)
    else:
        return trans_num


# 分段时间饼图数据
def feature_pie_data(json_data):
    day_section = []
    category_names = ['midnight', 'morning', 'noon', 'afternoon', 'evening', 'night']
    section_visit_count = [0] * 6
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
        temp_section['scale'] = pie_data_scale(min(section_visit_count), max(section_visit_count), 5.0, 70.0,
                                               section_visit_count[j], False)
        temp_section['sort'] = j
        day_section.append(temp_section)

    return day_section


# 给定年月返回月份的天数
def get_num_of_days_in_month(is_leap_year, month):
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif month in (4, 6, 9, 11):
        return 30
    elif is_leap_year:
        return 29
    else:
        return 28


# 生成空白日历
def generate_calender_list(year):
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        is_leap_year = True
    else:
        is_leap_year = False

    year_list = {}
    for i in range(1, 13):
        temp_month = {}
        lens = get_num_of_days_in_month(is_leap_year, i)
        for j in range(1, lens + 1):
            temp_month[j] = 0
        year_list[i] = temp_month

    return year_list


# 计算日历图数据
def count_calender_data(json_data):
    print json_data
    calender_data = {}
    years = []
    date_list = []
    pre_data = calender_day_section(json_data)
    for i in json_data:
        temp_time = i['lastVisitTime'].split('/')
        temp_year = int(temp_time[0])
        if temp_year not in years:
            years.append(temp_year)

    for j in years:
        temp_year_list = generate_calender_list(j)
        calender_data[j] = temp_year_list

    value_list = []
    for i in pre_data.keys():
        for j in pre_data[i].keys():
            for k in pre_data[i][j].keys():
                for p in pre_data[i][j][k].keys():
                    if p != 'total':
                        if 11 <= p < 14 or 17 <= p < 19:
                            calender_data[i][j][k] += float(
                                pre_data[i][j][k][p]*1.0/pre_data[i][j][k]['total'] * 5.0)
                        elif p == 23 or 0 <= p < 8:
                            calender_data[i][j][k] += float(
                                pre_data[i][j][k][p] * 1.0 / pre_data[i][j][k]['total'] * 10.0)
                if calender_data[i][j][k] == 0:
                    calender_data[i][j][k] = 1.0
                value_list.append(calender_data[i][j][k])

    print value_list
    for i in calender_data.keys():
        for j in calender_data[i].keys():
            for k in calender_data[i][j].keys():
                if calender_data[i][j][k] != 0:
                    calender_data[i][j][k] = pie_data_scale(
                        min(value_list), max(value_list), 1.0, 7.0, calender_data[i][j][k], True)
                temp_date = {}
                times = str(i) + '/' + str(j) + '/' + str(k)
                temp_date['date'] = times
                temp_date['level'] = calender_data[i][j][k]
                date_list.append(temp_date)

    return date_list


# 日历图数据预计算
def calender_day_section(json_data):
    form = dm.load_data("files/category_list.json")
    each_day_section = {}
    for i in json_data:
        temp_date = i['lastVisitTime'].split('/')
        temp_year = int(temp_date[0])
        temp_month = int(temp_date[1])
        temp_day = int(temp_date[2])
        clocks = temp_date[3].split(':')
        temp_hour = int(clocks[0])
        temp_url = i['url']
        if 'www.' in temp_url:
            temp_url = temp_url.replace('www.', '')

        if each_day_section.get(temp_year) is None:
            each_day_section[temp_year] = {}
            each_day_section[temp_year][temp_month] = {}
            each_day_section[temp_year][temp_month][temp_day] = {}
            each_day_section[temp_year][temp_month][temp_day]['total'] = i['visitCount']
            if form.get(temp_url) is None or form.get(temp_url) == 'Education' or form.get(temp_url) == 'Search':
                each_day_section[temp_year][temp_month][temp_day][temp_hour] = i['visitCount']
            else:
                each_day_section[temp_year][temp_month][temp_day][temp_hour] = 0

        elif each_day_section[temp_year].get(temp_month) is None:
            each_day_section[temp_year][temp_month] = {}
            each_day_section[temp_year][temp_month][temp_day] = {}
            each_day_section[temp_year][temp_month][temp_day]['total'] = i['visitCount']
            if form.get(temp_url) is None or form.get(temp_url) == 'Education' or form.get(temp_url) == 'Search':
                each_day_section[temp_year][temp_month][temp_day][temp_hour] = i['visitCount']
            else:
                each_day_section[temp_year][temp_month][temp_day][temp_hour] = 0

        elif each_day_section[temp_year][temp_month].get(temp_day) is None:
            each_day_section[temp_year][temp_month][temp_day] = {}
            each_day_section[temp_year][temp_month][temp_day]['total'] = i['visitCount']
            if form.get(temp_url) is None or form.get(temp_url) == 'Education' or form.get(temp_url) == 'Search':
                each_day_section[temp_year][temp_month][temp_day][temp_hour] = i['visitCount']
            else:
                each_day_section[temp_year][temp_month][temp_day][temp_hour] = 0

        else:
            each_day_section[temp_year][temp_month][temp_day]['total'] += i['visitCount']
            if each_day_section[temp_year][temp_month][temp_day].get(temp_hour) is None:
                if form.get(temp_url) is None or form.get(temp_url) == 'Education' or form.get(temp_url) == 'Search':
                    each_day_section[temp_year][temp_month][temp_day][temp_hour] = i['visitCount']
                else:
                    each_day_section[temp_year][temp_month][temp_day][temp_hour] = 0
            else:
                if form.get(temp_url) is None or form.get(temp_url) == 'Education' or form.get(temp_url) == 'Search':
                    each_day_section[temp_year][temp_month][temp_day][temp_hour] += i['visitCount']

    return each_day_section

# calender_day_section(dm.load_data("files/cut_history.json"))

# print count_calender_data(dm.load_data("files/cut_history.json"))
# words_cloud_data(dm.load_data("files/cut_history.json"))
# print json.dumps(calc_topn(dm.load_data("files/cut_history.json")), ensure_ascii=False)
