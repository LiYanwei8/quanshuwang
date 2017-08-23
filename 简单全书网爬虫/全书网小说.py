# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1

import urllib2
import re
import random
import os

# 可以是User-Agent列表，也可以是代理列表
ua_list = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
]

# 在User-Agent列表里随机选择一个User-Agent
user_agent = random.choice(ua_list)

# 小说分类
sort_list = ['玄幻魔法', '武侠修真', '女频言情', '历史军事', '侦探推理', '网游动漫', '科幻小说', '恐怖灵异', '美文同人']

def getSortList(sort):
    '''
        获取小说分类列表
        @sort :1 玄幻魔法 2 武侠修真 3 女频言情 4 历史军事
         5 侦探推理 6 网游动漫 7 科幻小说 8 恐怖灵异 9 美文同人
    '''
    url = "http://www.quanshuwang.com/map/%d.html"%sort
    # 构造一个请求
    requests = urllib2.Request(url);
    requests.add_header("User-Agent",user_agent)
    response = urllib2.urlopen(requests)
    html = response.read()
    # 把目标编码转换成Unicode
    html =  html.decode("gbk")
    # 再把Unicode转换成utf-8
    html = html.encode("utf-8")
    # 正则表达式
    # 匹配 <a href="/book/0/149/index.html" target="_blank">将夜</a>
    # 取出地址和书名
    reg = r'<a href="(/book/.*?)" target="_blank">(.*?)</a>'
    return re.findall(reg,html)


def getChapterList(url):
    '''获取小说章节列表
    :param url: 小说url
    :return: 小说章节列表
    '''
    # http://www.quanshuwang.com/book/0/149/index.html
    url = "http://www.quanshuwang.com%s"%url
    requests = urllib2.Request(url)
    requests.add_header("User-Agent",user_agent)
    response = urllib2.urlopen(requests)
    html = response.read()
    html =  html.decode("gbk").encode("utf-8")
    # <a href="34333.html" title="开头">开头</a>
    reg = r'<li><a href="(.+?)" title=".*?">(.*?)</a></li>'
    return re.findall(reg,html)


def getChapter(novelurl,chapterurl):
    '''获取小说章节内容
    :param novelurl: 小说地址
    :param chapterurl: 章节地址
    :return: 返回章节内容
    '''
    # http://www.quanshuwang.com/book/0/149/34334.html
    str = novelurl.split('/')[-1]
    url = "http://www.quanshuwang.com%s"%novelurl.replace(str,chapterurl)
    # print url
    requests = urllib2.Request(url)
    requests.add_header("User-Agent", user_agent)
    response = urllib2.urlopen(requests)
    html = response.read()
    #  UnicodeDecodeError: 'gbk' codec can't decode bytes in position 7036-7037: illegal multibyte sequence
    html = html.decode("gbk").encode("utf-8")
    # ()特殊字符要专义 style5\(\);</script>
    # 文章的结尾<script type="text/javascript">style6();</script>
    reg = r'style5\(\);</script>([\s\S]*)<script type="text/javascript">style6'

    return re.findall(reg,html)[0]


def main():
    '''
        主函数
    '''
    # 小说url队列 小说id 和详细页面数据队列
    novelcount = 0
    novelnumber = 0;
    for sort in xrange(1, 10):
        # 指定小说分类目录的路径和目录名
        print sort_list[sort - 1]
        sortFilename = "./Data/" +  sort_list[sort - 1]
        # 如果目录不存在，则创建目录
        if (not os.path.exists(sortFilename)):
            os.makedirs(sortFilename)

        for novel in getSortList(sort):
            # 所有类型小说的名字和url
            novelurl = novel[0]
            novelname = novel[1]
            # 将小说目录放在分类目录下
            subFilename = sortFilename + '/' + novelname
            # 如果目录不存在，则创建目录
            if (not os.path.exists(subFilename)):
                os.makedirs(subFilename)

            for chapter in getChapterList(novelurl):
                # 小说所有的章节名和列表url
                chapterurl = chapter[0]
                chaptername = chapter[1]
                str = getChapter(novelurl, chapterurl)

                print chaptername

                # 数据清洗,去掉&nbsp和<br />
                str = str.replace('&nbsp;',' ').replace(r'<br />','')

                # 文件名为chaptername
                filename = chaptername
                filename += ".txt"
                fp = open(subFilename + '/' + filename, 'w')
                fp.write(str)
                fp.close()
                print '存储了' + novelname + '的' + filename


            novelcount += 1
            novelnumber = novelcount
            print '存储了 ' + str(novelcount) + ' 本小说'

    print "共%d本小说" % novelnumber


if __name__ == "__main__":
    '''
        主程序入口
    '''
    main()