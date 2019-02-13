# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import json
import pymysql
import csv
import numpy as np
import pandas as pd


#----------------------------------------------------------------------
def sqlConnect():
    """打开数据库连接"""
    return pymysql.connect(host="localhost",user='root',passwd='123456',db='xueqiudata', charset='utf8')

    
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
        
        


class XueqiuPipeline(object):
    #----------------------------------------------------------------------
    def __init__(self):
        """"""
        # 打开数据库连接
        self.conn = sqlConnect()
        
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
        
        
        
        
        
class MainFinancePipeline(object):
    #----------------------------------------------------------------------
    def __init__(self):
        """"""
        # 打开数据库连接
        self.conn = sqlConnect()
        
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.conn.cursor()        
        
        
    def close_spider(self, spider):
        #关闭游标对象
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()  
            
    def process_item(self, item, spider):
        tableData=item['table']
        infoData=pd.DataFrame(tableData[0])
        for ld in data:
            pdData=pd.DataFrame(ld)
            infoData=infoData.append(pdData.loc[0], ignore_index=True) 
        infoData.drop(1)
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
class XueQiuSQL(object):
    """数据输入到MySQL数据库中"""
    
    INSTER_STATEMENT={'zyzb':'(股票代码,股票名称,报表名称,净资产收益率（比）,每股净资产（元）,每股经营现金流（元）,每股收益（元）,每股资本公积金（元）,每股未分配利润（元）,总资产报酬率（比）,销售净利率（比）,销售毛利率（比）,营业收入（元）,营业收入同比增长（比）,净利润（元）,净利润同比增长（比）,扣非净利润（元）,扣非净利润同比增长（比）,净资产收益率_摊薄（比）,人力投入回报率（比）,资产负债率（比）,流动比率,速动比率,权益乘数（比）,产权比率（比）,股东权益比率（比）,现金流量比率（比）,存货周转天数（天）,应收账款周转（天）,应付账款周转天数（天）,现金循环周期（天）,营业周期（天）,总资产周转率（次）,存货周转率（次）,应收账款周转率（次）,应付账款周转率（次）,流动资产周转率（次）,固定资产周转率（次）) VALUES ',
                      'lrb':'VALUES (%s,%s,%s,%s,%s,%s,%s)',
                      'zcfzb':'VALUES (%s,%s,%s,%s,%s,%s,%s)',
                      'xjllb':'VALUES (%s,%s,%s,%s,%s,%s,%s)'
                      }

    #----------------------------------------------------------------------
    def __init__(self,tableName):
        """Constructor"""
        self.tableName = tableName
        # 打开数据库连接
        self.conn = pymysql.connect(host="localhost",user='root',passwd='123456',db='xueqiudata', charset='utf8')
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.conn.cursor() 
    
    #----------------------------------------------------------------------
    def close_sql(self):
        """关闭游标对象和数据库连接"""
        #关闭游标对象
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()  
        
    #----------------------------------------------------------------------
    def insert_sql(self, sqlVal):
        """
        功能：将抓取到的数据输入到数据库中
        输入：sqlVal,待输入的数组
        """
        sqlCommand='INSERT INTO ' + self.tableName + ' ' + self.INSTER_STATEMENT[self.tableName] 
        strValue = str(sqlVal).replace('[','(').replace(']',')').replace('None','NULL')    
        try:
            self.cursor.execute(sqlCommand + strValue[1:-1])
            self.conn.commit()
        except:
            self.conn.rollback()

        

    
            

        
        
 
