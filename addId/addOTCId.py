# -*- coding: UTF-8_general_ci -*-

import requests
import request
import json
import pymysql
import datetime
import pandas as pd
import lxml,html5lib
from pandas import Series, DataFrame
import time

yesterday = datetime.datetime.now().strftime("%Y%m%d")
#抓取上市櫃股票代碼名稱－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
db =pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='onmarket' , charset='utf8')
cursor = db.cursor()

odf=pd.read_html('http://isin.twse.com.tw/isin/C_public.jsp?strMode=4',encoding='big5hkscs',header=0)
otcdf=odf[0][odf[0][u'產業別'] > '0']
del otcdf[u'國際證券辨識號碼(ISIN Code)'],otcdf[u'CFICode'],otcdf[u'備註']
odf2=otcdf[u'有價證券代號及名稱'].str.split(' ', expand=True)
odf2 = odf2.reset_index(drop=True)
otcdf = otcdf.reset_index(drop=True)
for i in odf2.index:
    if u'　' in odf2.iat[i,0]:
        odf2.iat[i,1]=odf2.iat[i,0].split(u'　')[1]
        odf2.iat[i,0]=odf2.iat[i,0].split(u'　')[0]
otcdf=odf2.join(otcdf)
otcdf=otcdf.rename(columns = {0:u'股票代號',1:u'股票名稱'})
del otcdf[u'有價證券代號及名稱'],otcdf[u'上市日']
otcsid = otcdf[u'股票代號']
otcname = otcdf[u'股票名稱']
print otcsid
print otcname
#－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
o = 0
for o in range(len(otcsid)):
        if (db):
            print otcsid+'searched';
        osql = """CREATE TABLE IF NOT EXISTS `""" + osid + """`(
                        ID INT AUTO_INCREMENT PRIMARY KEY,
                        date  varchar(30) ,
                        sid varchar(20),
                        name varchar(20),  
                        shareTrades	varchar(30),
                        turnover varchar(30) ,
                        open varchar(30),
                        high varchar(30) ,
                        low varchar(30) ,
                        closing varchar(30))
                        ENGINE = InnoDB,
                        CHARSET=utf8,
                        COLLATE utf8_unicode_ci;"""
        ost = """select count(*) from `""" + sid + """`"""
        osearchTable = cursor.execute(ost)
        if (osearchTable):
            print u'資料表已存在';
        else:
            try:
                cursor.execute(osql);
            except:
                pass
    time.sleep(1)
db.close()