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
from addStockId import mname,msid
from headers import header
start = time.time()
starttime = int(time.strftime("%M", time.localtime()))
yesterday = datetime.datetime.now().strftime("%Y%m%d")

l = 0
for l in range(len(msid)):
    db = pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='Listing',
                         charset='utf8')
    cursor = db.cursor()
    asid = msid[l]
    name = mname[l]
    params = {"date": yesterday,
              "stockNo": asid}
    conntime = b = int(time.strftime("%M", time.localtime()))
    intervalList = [1, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 59] * 200
    proxiesList = ["http://60.249.6.104:8080", "http://60.249.6.105:8080",
                   "http://60.249.6.104:8080", "http://192.168.1.3:8080"] * 1000
    if conntime - starttime >= intervalList[l]:
        headers = {'user-agent': header[l]}
        proxies = {'proxy': proxiesList[l]}
    else:  # 找可用IP塞到list
        headers = {'user-agent': "my-app/0.0.1"}
        proxies = {'proxy': "http://192.168.1.3:8080"}
    time.sleep(3)
    res = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY',
                       params=params, headers=headers, proxies=proxies)
    try:
        allData = json.loads(res.text)
    except:
        pass;
    if ('data' in allData.keys()):
        _data = allData['data']
        for i in range(len(_data)):
            print _data[i][0]
            insert = (
                """INSERT  INTO `""" + asid + """` (`Date`, `sid`, `name`, `shareTrades`, `turnover`, `open`, `high`, `low`, `closing`,`grossspread`,`tradingvolume`,`time`) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)""")
            da = (
                _data[i][0], asid, name, _data[i][1], _data[i][2], _data[i][3], _data[i][4], _data[i][5],
                _data[i][6],
                _data[i][7], _data[i][8], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            cursor.execute(insert, da)
            db.commit()
    print asid + 'inserted'
    db.close()
end = time.time()
print end - start
# 引入thread 同時上傳上市上貴資料
