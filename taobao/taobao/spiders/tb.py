# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from taobao.items import TaobaoItem
import time


class TbSpider(scrapy.Spider):
    name = "tb"
    allowed_domains = ["taobao.com"]
    url = 'https://s.taobao.com/search?q=&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20171218&ie=utf8&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s='
    offset = 0
    start_urls = [url+str(offset)]

    
    def parse(self, response):
        body = response.body.decode('utf-8','ignore')
        pid = '"nid":"(.*?)"'
        pprice = '"view_price":"(.*?)"'
        pname = '"raw_title":"(.*?)"'
        paddress='"item_loc":"(.*?)"'
        allid = re.compile(pid).findall(body)
        allprice = re.compile(pprice).findall(body)
        allname = re.compile(pname).findall(body)
        alladdress = re.compile(paddress).findall(body)

        for i in range(len(allid)):
            nid = allid[i]
            nprice = allprice[i]
            nname = allname[i]
            naddress = alladdress[i]
            #print ,nid
            page_url = 'https://item.taobao.com/item.htm?spm=a230r.1.14.338.6c7f49c0innIMt&id='+str(nid)+'&ns=1&abbucket=3#detail'
            
            #将获取到每页的里面每个商品的URL转给下个函数，用meta将参数传递给下个request请求
            yield scrapy.Request(url = page_url,callback = self.next,meta = {'price':nprice,'name':nname,'address':naddress,'pn_id':nid})

        if self.offset>=440:
            self.offset+=44
            time.sleep(2)
            yield scrapy.Request(self.url+str(self.offset),callback = self.parse)

            
        
    def next(self,response):
        
        item = TaobaoItem()
        item['title'] = response.meta['name']
        item['price'] = response.meta['price']
        item['address'] = response.meta['address']
        item['link'] = response.url


