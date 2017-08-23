# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1

from UrlManager import UrlManager
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser
from DataOutput import DataOutput
import os
import threading

import logging
# 保存日志方便查看
logging.basicConfig(filename='logging.log',
                    format='%(asctime)s %(message)s',
                    filemode="w", level=logging.DEBUG)


class myThread(threading.Thread):
    def __init__(self, sort, sort_url, sortFilename):
        threading.Thread.__init__(self)
        self.sort = sort
        self.sort_url = sort_url
        self.sortFilename = sortFilename


        self.manager = UrlManager(self.sort)
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def run(self):
        print "启动 %d"%self.sort
        try:
            self.crawl(self.sort, self.sort_url, self.sortFilename)
        except:
            pass

    def crawl(self, sort, sort_url, sortFilename):
        # 添加入口URL
        # HTML下载器下载网页

        print sort_url
        html = self.downloader.download(sort_url)

        # HTML解析器抽取网页数据 所有的小说名和url
        novels = self.parser.novel_parser(sort_url, html)
        for novel in novels:
            novelurl = novel[0]
            novelurl = "http://www.quanshuwang.com%s" % novelurl
            novelname = novel[1]
            # print novelurl,novelname

            # 将小说目录放在分类目录下
            subFilename = sortFilename + '/' + novelname
            # 如果目录不存在，则创建目录
            if (not os.path.exists(subFilename)):
                os.makedirs(subFilename)

            html = self.downloader.download(novelurl)
            chapters = self.parser.chapterlist_parser(novelurl, html)
            # chapters = zip(*chapters)
            for chapter in chapters:
                chapterurl = chapter[0]
                str = novelurl.split('/')[-1]
                chapterurl = novelurl.replace(str, chapterurl)
                self.manager.add_new_url(chapterurl)

            print sort_list[sort -1] + "新添加" + "%d条url" % self.manager.new_url_size()
            # 判断url管理器中是否有新的url
            while (self.manager.has_new_url()):
                try:
                    # 从URL管理器获取新小说章节url
                    new_url = self.manager.get_new_url()

                    # HTML下载器下载网页
                    html = self.downloader.download(new_url)
                    # HTML解析器抽取网页数据
                    title, content = self.parser.chapter_parser(new_url, html)
                    # 数据存储器储存文件
                    self.output.store_data(title, content, subFilename)
                    print "已经抓取%s个链接" % self.manager.old_url_size()

                    urlsFilename = "./新旧url/"
                    # 如果目录不存在，则创建目录
                    if (not os.path.exists(urlsFilename)):
                        os.makedirs(urlsFilename)

                    # 存储set的状态
                    self.manager.save_progress(urlsFilename + 'new_urls_%d.txt'%sort, self.manager.new_urls)
                    self.manager.save_progress(urlsFilename + 'old_urls_%d.txt'%sort, self.manager.old_urls)

                except Exception, e:
                    print "crawl failed: " + e
                    p_rint = "crawl failed: " + e
                    logging.info(p_rint)


# 小说分类
sort_list = ['玄幻魔法', '武侠修真', '女频言情', '历史军事', '侦探推理', '网游动漫', '科幻小说', '恐怖灵异', '美文同人']

if __name__=="__main__":

    for sort in xrange(1, 10):
        # 指定小说分类目录的路径和目录名
        print sort_list[sort - 1]
        sortFilename = "./全书网/" +  sort_list[sort - 1]
        # 如果目录不存在，则创建目录
        if (not os.path.exists(sortFilename)):
            os.makedirs(sortFilename)
        thread = myThread(sort, "http://www.quanshuwang.com/map/%s.html"%sort,sortFilename)
        thread.start()

