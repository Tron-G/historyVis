# -*- coding:utf-8 -*-
import random
import ssl
import urllib2
import jieba
import codecs
from bs4 import BeautifulSoup


# 按标签爬取关键词序列
def grab_new_data(page_url, soup):
    res_data = {}
    res_data['url'] = page_url
    try:
        res_data['description'] = soup.find(attrs={"name": "description"})['content']
    except:
        print "##description error!##", res_data['url']
    try:
        res_data['keywords'] = soup.find(attrs={"name": "keywords"})['content']
    except:
        print "##keywords error!##", res_data['url']
    try:
        res_data['title'] = soup.find('title')
        strss = str(res_data['title'])
        strss = strss.replace('title', '')
        strss = strss.strip('<>/')
        res_data['title'] = strss.decode('utf8')
    except:
        print "##title error!##", res_data['url']
    return res_data


def get_text_data(root_url):
    root_url = 'https://' + root_url + '/'
    ip = ['121.31.159.197', '175.30.238.78', '124.202.247.110']
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
        'X-Forwarded-For': ip[random.randint(0, 2)]}
    ssl._create_default_https_context = ssl._create_unverified_context
    request = urllib2.Request(root_url, None, header)
    response = urllib2.urlopen(request)
    html_content = response.read()
    soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
    data = grab_new_data(root_url, soup)
    # print data['description']
    # print data['keywords']
    key_strs = ''
    try:
        key_strs = data['title']
    except:
        print "##no title##", data['url']
    try:
        key_strs += ',' + data['keywords']
    except:
        pass
    try:
        key_strs += ',' + data['description']
    except:
        pass
    print key_strs
    calc_tf(separate(key_strs))


def spider(urls):
    for i in urls:
        try:
            get_text_data(i)
        except:
            print i
            print "##spider error##"


# 加载停用词表
def stopwords_list(file_path):
    stopwords = [line.strip() for line in codecs.open(file_path, 'r', encoding='utf-8').readlines()]
    return stopwords


# 分词
def separate(strs):
    try:
        text_content = strs
        depart_words = jieba.cut(text_content)
        stopwords = stopwords_list('./files/stopwords.txt')
        outstr = ''
        for word in depart_words:
            if word not in stopwords:
                if word != '\t' and word != ' ' and word != '\n' and word != u'\u3000':
                    outstr += word
                    outstr += "/"
        return outstr
    except:
        print "##separate error##\n"


# 关键词计算
def calc_tf(strs):
    line_str = strs.replace(' ', '')
    str_lis = line_str.split('/')

    Tf = 1.0
    tf = []

    for index in range(0, len(str_lis)):
        for j in range(0, len(str_lis)):  # Tf值计算
            if j == index:
                continue
            if str_lis[j] == str_lis[index] and str_lis[j] != "0":
                Tf = Tf + 1
                str_lis[j] = "0"

        Tf = float(Tf / (len(str_lis) - 1))
        tf.append(Tf)
        Tf = 1.0

    tf.pop()

    dic = {}
    for p in range(0, len(str_lis) - 1):  # 创建词-Tf值字典
        if str_lis[p] == "0":
            continue
        dic[str_lis[p]] = tf[p]

    key_dict = sorted(dic.iteritems(), key=lambda d: d[1], reverse=True)  # 关键词重要性排序

    # print json.dumps(keyDict, ensure_ascii=False)

    keywords = []
    for num in range(0, 5):  # 提取TF值前5的关键词
        keywords.append(key_dict[num][0])

    for i in keywords:
        print i
