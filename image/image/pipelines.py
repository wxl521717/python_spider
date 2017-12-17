# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib
import re
class ImagePipeline(object):
    def process_item(self, item, spider):

        for i in range(0,len(item['url'])):

            if len(item['url']) ==0:
                continue
            imgurl = item['url'][i]

            imgname = re.findall('http://724.169pp.net/169mm/(.*?).jpg',imgurl)[0]
            count = imgname.replace('/','_')


            urllib.urlretrieve(url=imgurl,filename=count+'.jpg')


        return item
