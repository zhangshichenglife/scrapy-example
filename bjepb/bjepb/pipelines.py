# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from bjepb.settings import *
from scrapy import Request
from scrapy.pipelines.files import FilesPipeline


class BjepbPipeline(object):

    def __init__(self, host, database, user, password, port, table):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.table = table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('HOST'),
            database=crawler.settings.get('DATABASE'),
            user=crawler.settings.get('USER'),
            password=crawler.settings.get('PASSWORD'),
            port=crawler.settings.get('PORT'),
            table=crawler.settings.get('TABLE')
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(self.host, self.user, self.password, self.database, self.port, charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = "insert into %s (%s) values (%s)" % (self.table, keys, values)
        self.cur.execute(sql, tuple(data.values()))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()


class PdfPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        file_name = request.url.split('/')[-2] + '.pdf'
        return file_name

    def get_media_requests(self, item, info):
        yield Request(dict(item).get('text_url'))

    def item_completed(self,result,item,info):
        pass

