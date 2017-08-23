# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1

import re

class HtmlParser(object):

    def novel_parser(self,sort_url,html):
        '''
        用于解析网页内容抽取URL和数据
        :param page_url: 下载页面的URL
        :param html_cont: 下载的网页内容
        :return:返回URL和数据
        '''
        if sort_url is None or html is None:
            return
        # 正则表达式
        # 匹配 <a href="/book/0/149/index.html" target="_blank">将夜</a>
        # 取出地址和书名
        reg = r'<a href="(/book/.*?)" target="_blank">(.*?)</a>'
        return re.findall(reg, html)

    def chapterlist_parser(self,novel_url,html):
        '''
        抽取新的URL集合
        :param url: 下载页面的URL
        :return: 返回新的URL集合
        '''
        # <a href="34333.html" title="开头">开头</a>
        reg = r'<li><a href="(.+?)" title=".*?">(.*?)</a></li>'
        return re.findall(reg, html)

    def chapter_parser(self,chapter_url,html):
        '''
        抽取有效数据
        :param url:下载页面的URL
        :return:返回有效数据
        '''
        # 标题
        reg1 = r'<strong class="l jieqi_title">([\s\S]*)</strong>'

        # 文章的结尾<script type="text/javascript">style6();</script>
        reg = r'style5\(\);</script>([\s\S]*)<script type="text/javascript">style6'


        return re.findall(reg1,html)[0],re.findall(reg, html)[0]
