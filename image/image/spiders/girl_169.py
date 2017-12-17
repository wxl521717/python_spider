# -*- coding: utf-8 -*-
import scrapy
from image.items import ImageItem
from scrapy.http import Request
class Girl169Spider(scrapy.Spider):
    name = "girl_169"
    allowed_domains = ["169mi.com"]
    start_urls = [
        'http://www.169mi.com/'
    ]
    
    num=1
    def parse(self, response):
        urldata = response.xpath('//div[@class="hd_nav"]/div[@class="w1000"]//a/@href').extract()
        title_list = response.xpath('//div[@class="hd_nav"]/div[@class="w1000"]//a//text()').extract()

        xiyang_url = urldata[4]
        print xiyang_url
        xiyang_title= title_list[4]

        yield Request(url = xiyang_url,callback=self.next)

    def next(self,response):

        page_link  = response.xpath('//ul[@class="product01"]//li/a/@href').extract()
        for i in range(1,328+1):
            all_link = response.url+'list_4_'+ str(i) + '.html'
            yield scrapy.Request(url = all_link,callback = self.next2)

    def next2(self,response):
        urllist = response.xpath('//ul[@class="product01"]//li/a/@href').extract()
        titles = response.xpath('//ul[@class="product01"]//li/a/p/text()').extract()

        for i in range(0,len(urllist)):
            get_girl_image = urllist[i]
            yield scrapy.Request(url = get_girl_image,callback = self.next3)

    def next3(self,response):
        real_list = response.xpath('//div[@class="dede_pages"]/ul[@class="pagelist"]//li/a/text()').extract()
        real_num = real_list[2:-1]
        #print real_num
        #print response.url

        for i in range(len(real_num)):
            girl_page_url = response.url.replace('.html','_')+str(real_num[i])+'.html'
            #print girl_page_url
            yield scrapy.Request(url = girl_page_url,callback = self.next4)

    def next4(self,response):

        item = ImageItem()
        item['url'] = response.xpath('//div[@class="big_img"]//p[@align="center"]/img/@src').extract()

        yield item