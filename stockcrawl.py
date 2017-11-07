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
df=pd.read_html('http://isin.twse.com.tw/isin/C_public.jsp?strMode=2',encoding='big5hkscs',header=0)
newdf=df[0][df[0][u'產業別'] > '0']
del newdf[u'國際證券辨識號碼(ISIN Code)'],newdf[u'CFICode'],newdf[u'備註']
df2=newdf[u'有價證券代號及名稱'].str.split(' ', expand=True)
df2 = df2.reset_index(drop=True)
newdf = newdf.reset_index(drop=True)
for i in df2.index:
    if u'　' in df2.iat[i,0]:
        df2.iat[i,1]=df2.iat[i,0].split(u'　')[1]
        df2.iat[i,0]=df2.iat[i,0].split(u'　')[0]
newdf=df2.join(newdf)
newdf=newdf.rename(columns = {0:u'股票代號',1:u'股票名稱'})
del newdf[u'有價證券代號及名稱'],newdf[u'上市日']
newsid = newdf[u'股票代號']
newname = newdf[u'股票名稱']
print newname[1]
'''
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
    osid = otcsid[o]
    oname = otcname[o]
    params = {"date": yesterday,
              "stockNo": osid}
    headers = {'user-agent': 'my-app/0.0.1'}
    res = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY',
                       params=params).decode("utf-8")
    allData = json.loads(res.text)
    if ('data' in allData.keys()):
        oday = allData['data']
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
        cursor.execute(osql)
        for w in range(len(oday)):
            insert = ("""INSERT  INTO `""" + osid + """` (`Date`, `sid`, `name`, `shareTrades`, `turnover`, `open`, `high`, `low`, `closing`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""")
            # ON DUPLICATE KEY UPDATE (`Date`,`sid`,`name`,`shareTrades`,`turnover`,`over`,`high`,`low`,`closing`)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)有更新，無新增
            oda = (oday[i][0], osid, oname, oday[i][1], oday[i][2], oday[i][3], oday[i][4], oday[i][5], oday[i][6])
            cursor.execute(insert,oda)
            db.commit()
    time.sleep(1)
'''
db =pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='onmarket' , charset='utf8')
cursor = db.cursor()
if (db):
    print 'good';

l = 0
for l in range(len(newsid)):
    sid = newsid[l]
    name = newname[l]
    params = {"date": yesterday,
              "stockNo": sid}
    headers = {'user-agent': 'my-app/0.0.1'}
    res = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY',
                       params=params)
    allData = json.loads(res.text)
    if(allData):
        print sid+u'有資料喔';
    if ('data' in allData.keys()):
        print 'data exists';
        day = allData['data']
        sql = """CREATE TABLE IF NOT EXISTS `""" + sid + """`(
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
        st = """select count(*) from `"""+sid+"""`"""
        searchTable = cursor.execute(st)
        if (searchTable):
            print u'資料表已存在';
        else:
            cursor.execute(sql);
        for i in range(len(day)):
            insert = ("""INSERT  INTO `""" + sid + """` (`Date`, `sid`, `name`, `shareTrades`, `turnover`, `open`, `high`, `low`, `closing`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""")
            # ON DUPLICATE KEY UPDATE (`Date`,`sid`,`name`,`shareTrades`,`turnover`,`over`,`high`,`low`,`closing`)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)有更新，無新增
            da = (day[i][0], sid, name, day[i][1], day[i][2], day[i][3], day[i][4], day[i][5], day[i][6])
            cursor.execute(insert,da)
            db.commit()
            if(insert):
                print 'inserted';
    time.sleep(1)

db.close()

#引入thread 同時上傳上市上貴資料