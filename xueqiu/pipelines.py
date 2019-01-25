# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import json
import pymysql
import csv



class XueqiuPipeline(object):
    #----------------------------------------------------------------------
    def __init__(self):
        """"""
        # 打开数据库连接
        self.conn = pymysql.connect(host="localhost",user='root',passwd='123456',db='xueqiudata', charset='utf8')
        
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.conn.cursor()        
        
        
    def close_spider(self, spider):
        #关闭游标对象
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()  
            
    def process_item(self, item, spider):
        try:
            sql='INSERT INTO gsjj ' \
                '(stock_code,SH_SZ,org_name_cn,main_operation_business,' \
                'org_cn_introduction,postcode,org_website) ' \
                'VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")'
            info=dict(item)
            self.cursor.execute(sql %(info['stock_code'],info['SH_SZ'],
                                      info['org_name_cn'],info['main_operation_business'],
                                      info['org_cn_introduction'],info['postcode'],info['org_website']))
            self.conn.commit() 
            
        except:
            #关闭游标对象
            self.cursor.close()
            # 关闭数据库连接
            self.conn.close()  
        finally:
            return item
        
        
########################################################################
class SubjectPipeline(object):
    """提取沪深两市的股票代码的管道"""

    #----------------------------------------------------------------------
    def __init__(self):
        self.csvFile = open("xueqiuSubject.csv", 'a',newline="")
        self.csvWriter = csv.writer(self.csvFile,dialect='excel')
        self.csvWriter.writerow(['股票代码','股票名称','股票链接'])
        
    def process_item(self, item, spider):    
        
        try:           
            self.csvWriter.writerows(zip(item['stock_symbol'],item['stock_name'],item['stock_url']))        
        except:
            self.csvFile.close()
        finally:
            return item  
        
        
    def close_spider(self, spider):
        self.csvFile.close()
        
        
    
    
            

        
        
 
