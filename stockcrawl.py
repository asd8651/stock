# -*- coding: UTF-8_general_ci -*-

import requests
import request
import json
import pymysql
import datetime
import pandas as pd
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
try:
    # sql = "DELE TE FROM `stockData` WHERE sid = '2344'"# 刪除
    # cursor.execute(sql)
    cursor.execute(insert, data)
    db.commit()
except:
    print "error"

#抓股票代號轉陣列用for迴圈

