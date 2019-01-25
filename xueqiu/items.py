# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XueqiuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #股票代码
    stock_code=scrapy.Field()
    #上证还是沪深
    SH_SZ=scrapy.Field()
    #公司名称
    org_name_cn=scrapy.Field()
    #主营业务
    main_operation_business=scrapy.Field()
    #公司简介
    org_cn_introduction=scrapy.Field()
    #邮政编码
    postcode=scrapy.Field()
    #公司网站
    org_website=scrapy.Field()
    pass


class SubjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #股票代码
    stock_symbol=scrapy.Field()
    #股票名称
    stock_name=scrapy.Field()
    #股票链接
    stock_url=scrapy.Field()
    pass