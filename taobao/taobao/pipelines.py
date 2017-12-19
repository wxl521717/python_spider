# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class TaobaoPipeline(object):
    def __init__(self):
        self.client = pymsql.connect(
            host = '127.0.0.1',
            port = 3306,
            user = 'root'
            passwd = '*****'
            charset = 'utf-8'
            )
        self.cur = self.client.cousor()
    def process_item(self, item, spider):
        sql = 'insert into shop(link,title,price,address)values(%s,%s,%f,%s)'
        ls = (item['link'],item['link'],item['price'],item['address'])
        self.cur.execute(sql,ls)
        self.client.commit()
        return item
