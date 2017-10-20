# -*- coding: UTF-8_general_ci -*-

import requests
import json
import pymysql
import datetime
import pandas as pd
from pandas import Series, DataFrame





yesterday = datetime.datetime.now().strftime("%Y%m%d")
params = {"date": yesterday,
          "stockNo":"2344"}
res = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY',
                     params=params)
allData = json.loads(res.text)
#fields = json.dumps(fie, encoding="UTF-8", ensure_ascii=False) 轉換為str
today = allData['data'][-1]
date = today[0]
open = today[3]
high = today[4]
low = today[5]
closing = today[6]
shareTrades = today[1]
turnover = today[2]
dataDict = {'date' : date,'open': open,'high': high,'low':low,'closing':closing,'shareTrades':shareTrades,'turnover':turnover}
print dataDict['date']
#print type(data)編碼類型
db = pymysql.connect("localhost","root","asd865100","stock",charset="utf8")
cursor = db.cursor()
#改資料庫 無法蓮接到
sql = """INSERT INTO `stockData` (`Date`, `sid`, `name`, `shareTrades`, `turnover`, `open`, `high`, `low`, `closing`, `volume`, `transaction`)
VALUES (dataDict['date'], '2330', '台積電', dataDict['shareTrades'],dataDict['turnover'],dataDice['open'],dataDice['high'],dataDice['low'],dataDice['closing']);"""
#新增
#sql = "DELETE FROM `stockData` WHERE sid = '2330'"; 刪除

try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()