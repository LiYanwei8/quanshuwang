# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1

class DataOutput(object):

    def __init__(self):
        self.datas=[]
    def store_data(self,title,content,subFilename):
        if title is None or content is None:
            return
        # 数据清洗,去掉&nbsp;和<br />
        content = content.replace('&nbsp;',' ').replace(r'<br />','')
        title = title.replace('全书网','')

        # 文件名为title
        filename = title
        filename += ".txt"
        fp = open(subFilename + '/' + filename, 'w')
        fp.write(content)
        fp.close()
        print '存储了' + filename
