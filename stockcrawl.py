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
day = allData['data']
date = str(day[-1][0])

#print type(data)編碼類型
db = pymysql.connect("localhost","root","asd865100","stock",charset="utf8")
cursor = db.cursor()
#新增
#insert = ("INSERT ignore  INTO stockdata (`Date`, `sid`, `name`, `shareTrades`, `turnover`, `open`, `high`, `low`, `closing`)"
  #        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
#data = (date, '2330','台積電',shareTrades,turnover,open,high,low,closing)
'''try:
    # sql = "DELE TE FROM `stockData` WHERE sid = '2344'"# 刪除
    # cursor.execute(sql)
    cursor.execute(insert, data)
    db.commit()
except:
    print "error"
'''

l = 0
for l in range(len(day)):
    insert = ("INSERT ignore  INTO `2330` (`Date`, `sid`, `name`, `shareTrades`, `turnover`, `open`, `high`, `low`, `closing`)"
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    data = (day[l][0], '2330', u'台積電', day[l][1], day[l][2], day[l][3], day[l][4], day[l][5], day[l][6])
    cursor.execute(insert, data)
    db.commit()
db.close()

#可傳到資料庫 不過要一筆一筆用