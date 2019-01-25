# -*- coding: utf-8 -*-

import scrapy
import json
from xueqiu.items import  XueqiuItem


class XueQiuSpider(scrapy.spiders.Spider):
    name = 'xueqiuMainFinance'
    allowed_domains = ['xueqiu.com']
    start_urls = ['https://stock.xueqiu.com/v5/stock/f10/cn/company.json?symbol=SZ000333',
              'https://stock.xueqiu.com/v5/stock/f10/cn/company.json?symbol=SZ000568']
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

    def start_requests(self):        

        for url in self.start_urls:
            yield scrapy.Request(url,headers = self.headers)

        
    def parse(self,response):
        item=XueqiuItem()
        Info=json.loads(response.body)
        url=response.url
        
        item['stock_code']=url[-6:]
        item['SH_SZ']=url[-8:-6]
        item['org_name_cn']=Info['data']['company']['org_name_cn']
        item['main_operation_business']=Info['data']['company']['main_operation_business']
        item['org_cn_introduction']=Info['data']['company']['org_cn_introduction']
        item['postcode']=Info['data']['company']['postcode']
        item['org_website']=Info['data']['company']['org_website']
        
        return item
  

