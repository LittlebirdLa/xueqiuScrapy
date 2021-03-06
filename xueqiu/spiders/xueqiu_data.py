# -*- coding: utf-8 -*-

import scrapy
import json
from xueqiu.items import  XueqiuItem


class XueQiuDataSpider(scrapy.spiders.Spider):
    name = 'xueqiuData'
    allowed_domains = ['xueqiu.com']
    general_urls = {'zyzb':'https://stock.xueqiu.com/v5/stock/finance/cn/indicator.json?symbol=%s&type=all&is_detail=true&count=60',
                    'lrb':'https://stock.xueqiu.com/v5/stock/finance/cn/income.json?symbol=%s&type=all&is_detail=true&count=60',
                    'zcfzb':'https://stock.xueqiu.com/v5/stock/finance/cn/balance.json?symbol=%s&type=all&is_detail=true&count=60',
                    'xjllb':'https://stock.xueqiu.com/v5/stock/finance/cn/cash_flow.json?symbol=%s&type=all&is_detail=true&count=60'
                    }
              
    headers = {
       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
       "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "device_id=70c8f2dd6f5bd13668859ee6f56cb3ac; s=ew11369bj3; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=6fd1b06ca15557cd35c86eb06cfe551004e33094; xq_a_token.sig=ukIyEEX-ALlEOj5RbvJG6pg1wjs; xqat=6fd1b06ca15557cd35c86eb06cfe551004e33094; xqat.sig=A4XanfKwGre4MwoRwSHi9jqAzJo; xq_r_token=058a28e23c8530d0e70e81665ae1b6a845a7bd36; xq_r_token.sig=y5KVRyvZMBMK0MX5E3rYyLXwIXo; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=7670359447; u.sig=XGTGq_ZAPQ8JJ-XzIXpV_9Li-mw; bid=3d4e4d12323f38b549b541ec462ebb9f_jqqq3uj1; _ga=GA1.2.1588097421.1547293483; _gid=GA1.2.1604675860.1547293483; Hm_lvt_1db88642e346389874251b5a1eded6e3=1547131691,1547293483,1547300706,1547358419; snbim_minify=true; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1547374237",
        "Host": "stock.xueqiu.com",
        "Upgrade-Insecure-Requests": 1,
        "User-Agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"                
    }
 
    custom_settings = {'ITEM_PIPELINES': {'xueqiu.pipelines.XueqiuPipeline': 400}} 
    
    
    subjectData = csv.reader(open("xueqiuSubject.csv"))


    def start_requests(self): 
        for symbol,name,url in self.subjectData:
            if name != "股票名称" :
                for table,exampUrl in general_urls:
                    url=exampUrl % symbol
                    myMeta={'stock_name':name,'stock_symbol':symbol,'stock_table':table}
                    yield scrapy.Request(url,meta=myMeta,headers = self.headers,dont_filter=True) 
        
    def parse(self,response,need):
        item=XueqiuItem()
        Info=json.loads(response.body)
        url=response.url
        item['data']=Info['data']['list'] 
        item['stock_name']=response.meta['stock_name']
        item['stock_symbol']=response.meta['stock_symbol']
        item['stock_table']=response.meta['stock_table']
        return item


