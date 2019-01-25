# -*- coding: utf-8 -*-

import scrapy
import json
from xueqiu.items import  SubjectItem


class XueQiuSubjectSpider(scrapy.spiders.Spider):
    name = 'xueqiuSubject'
    allowed_domains = ['xueqiu.com']
    #直接输入一个通用url，使用时只需要改变其中page的值
    start_urls = ('https://xueqiu.com/hq#exchange=CN&firstName=1&secondName=1_0&page=%d'  % (i+1) for i in range(187))
    #url_general = 'https://xueqiu.com/stock/cata/stocklist.json?page=%d&size=90&order=desc&orderby=percent&type=11%%2C12'
    
    headers = {
       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
       "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "stock.xueqiu.com",
        "User-Agent":"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"                
    }
    
    custom_settings = {'ITEM_PIPELINES': {'xueqiu.pipelines.SubjectPipeline': 400},
                       'DOWNLOADER_MIDDLEWARES' : {'xueqiu.middlewares.AreaSpiderMiddleware': 543}                       
                       }    


    def start_requests(self):        
      
        #现在网站上查看“沪深一览”股票代码总共有多少页
        #for pageNum in range(5): 
            #url=self.url_general % (pageNum+1)
        for url in self.start_urls:
            yield scrapy.Request(url=url,headers = self.headers,dont_filter=True)

        
    def parse(self,response):
        item=SubjectItem()
        item['stock_symbol']=response.xpath("//*[@id='stockList']/div[1]/table/tbody/tr/td[1]/a/text()").extract()
        item['stock_name']=response.xpath("//*[@id='stockList']/div[1]/table/tbody/tr/td[2]/a/text()").extract()
        item['stock_url']=response.xpath("//*[@id='stockList']/div[1]/table/tbody/tr/td[1]/a/@href").extract()
        return item
  

