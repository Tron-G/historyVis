# -*- coding:utf-8 -*-
import Spider as sp
import Data_Manager as dm


# ↓↓↓↓ 定义top n ↓↓↓↓
topn = 10


# 计算top n主页网站
def calc_topn(json_datas):
    topn_urls = {}
    for i in json_datas:
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


dm.transform_data("files/history.json")
sp.spider(calc_topn(dm.load_data("files/cut_history.json")))

# calc_topn(load_datas())