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


#抓取上市櫃股票代碼名稱－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    #上市

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
    #上櫃
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
otcsid = otcdf[u'股票代號'].loc[0]
'''
#－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－


yesterday = datetime.datetime.now().strftime("%Y%m%d")
print yesterday
#print type(data)編碼類型
db =pymysql.connect(host='0.tcp.ngrok.io', port=12714, user='root', passwd='ncutim', db='onmarket' , charset='utf8')
cursor = db.cursor()

l = 0
for l in range(len(newsid)):
    sid = newsid[l]
    params = {"date": yesterday,
              "stockNo": sid}
    res = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY',
                       params=params)
    allData = json.loads(res.text)
    # fields = json.dumps(fie, encoding="UTF-8", ensure_ascii=False) 轉換為str
    day = allData['data']
    #search = "select * from`" + sid + "` WHERE ID = 1;"
    #if search == True:
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
    cursor.execute(sql)
    for i in range(len(day)):
        name = newname[l]
        insert = ("""INSERT  INTO `""" + sid + """` (`Date`, `sid`, `name`, `shareTrades`, `turnover`, `open`, `high`, `low`, `closing`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE Date = %s,sid = %s,name = %s,shareTrades = %s,turnover=%s,open = %s,high = %s,low = %s,closing = %s""")
        # ON DUPLICATE KEY UPDATE (`Date`,`sid`,`name`,`shareTrades`,`turnover`,`over`,`high`,`low`,`closing`)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)有更新，無新增
        da = (day[i][0], sid, name, day[i][1], day[i][2], day[i][3], day[i][4], day[i][5], day[i][6] , day[i][0], sid, name, day[i][1], day[i][2], day[i][3], day[i][4], day[i][5], day[i][6])
        cursor.execute(insert,da)
        db.commit()
    time.sleep(1)




