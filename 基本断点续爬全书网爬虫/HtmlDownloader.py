# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1

import urllib2
import random
import logging
# 保存日志方便查看
logging.basicConfig(filename='logging.log',
                    format='%(asctime)s %(message)s',
                    filemode="w", level=logging.DEBUG)

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

class HtmlDownloader(object):

    def download(self,url):
        if url is None:
            return None
        requests = urllib2.Request(url)
        requests.add_header("User-Agent", user_agent)
        try:
            response = urllib2.urlopen(requests)
            html = response.read()
            html = html.decode("gbk").encode("utf-8")
            return html
        except urllib2.HTTPError as e:
            if hasattr(e, 'code'):
                print 'error code:',e.code
                p_rint = 'error code:' + e.code
                logging.info(p_rint)


