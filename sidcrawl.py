# -*- coding: UTF-8_general_ci -*-

import requests
import request
import json
import pymysql
import datetime
import pandas as pd
import lxml,html5lib
from pandas import Series, DataFrame

yesterday = datetime.datetime.now().strftime("%Y%m%d")
params = {"date": yesterday,
          "stockNo":"2330"}
res = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY',
                     params=params)
allData = json.loads(res.text)
#fields = json.dumps(fie, encoding="UTF-8", ensure_ascii=False) 轉換為str
today = allData['data'][-1]
date = str(today[0])
open = today[3]
high = today[4]
low = today[5]
closing = today[6]
shareTrades = today[1]
turnover = today[2]
dataDict = {'date' : date,'open': open,'high': high,'low':low,'closing':closing,'shareTrades':shareTrades,'turnover':turnover}
#print type(data)編碼類型
db = pymysql.connect("localhost","root","asd865100","stock",charset="utf8")
cursor = db.cursor()
#新增
insert = ("INSERT ignore  INTO stockdata (`Date`, `sid`, `name`, `shareTrades`, `turnover`, `open`, `high`, `low`, `closing`)"
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
data = (date, '2330','台積電',shareTrades,turnover,open,high,low,closing)
'''try:
    # sql = "DELE TE FROM `stockData` WHERE sid = '2344'"# 刪除
    # cursor.execute(sql)
    cursor.execute(insert, data)
    db.commit()
except:
    print "error"
'''
#抓股票代號轉陣列用for迴圈
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
    #上櫃
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
print otcdf[u'股票代號']
#－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－