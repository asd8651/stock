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
    if ('data' in allData.keys()):
        day = allData['data']
        print day