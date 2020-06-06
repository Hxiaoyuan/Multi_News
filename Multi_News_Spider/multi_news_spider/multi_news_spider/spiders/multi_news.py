# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.project import get_project_settings
import os

''' 
INPUTS_TXT:1
SUMMARIES_TXT:1
AVAILABILITY_TXT:1
'''
settings = get_project_settings()
# INPUTS_TXT 、SUMMARIES_TXT 、AVAILABILITY_TXT
curSpiderType = "INPUTS_TXT"
# INPUT_RECORD_TXT、SUMMARIES_RECORD_TXT
curSpiderRecordType = "INPUT_RECORD_TXT"
writeList = []

proxy_host = '127.0.0.1'
proxy_port = '10809'  # 查看自己的端口  控制面板->Internet选项->internet属性里面的连接选项->局域网设置

proxy_user = ''
proxy_pass = ''

proxy_meta = 'http://%(user)s:%(pass)s@%(host)s:%(port)s' % {
    'host': proxy_host,
    'port': proxy_port,
    'user': proxy_user,
    'pass': proxy_pass,
}

proxy = proxy_host + ':' + proxy_port
proxies = 'http://' + proxy


class MultiNewsSpider(scrapy.Spider):
    name = 'multi_news'

    def start_requests(self):
        self.log("读取已爬取资料....")
        with open(settings[curSpiderRecordType], 'r') as read_f:
            for line in read_f:
                writeList.append(line.split('\n')[0])
        with open(settings[curSpiderType], 'r') as _input:
            for line in _input:
                line = line.split('\t')
                if line[1].strip() not in writeList:
                    req = scrapy.Request(url=line[0].strip(), callback=self.parse, meta={'proxy': proxies})
                    req.meta['filename'] = line[1].strip()
                    yield req

    def parse(self, response):
        filename = response.meta['filename']
        if response.status == 200:
            try:

                with open(f"{filename}", mode='w') as f:
                    f.write(response.text)
                    writeList.append(filename)

                    with open(settings[curSpiderRecordType], 'a+') as f1:
                        f1.write(filename + "\n")
            except FileNotFoundError:
                _dir = filename.split('/')
                os.makedirs(_dir[0].strip())

            self.log('Saved file %s' % filename)
