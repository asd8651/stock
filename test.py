# -*- coding: UTF-8_general_ci -*-
#上傳今天的個股資料到stockdata資料表
import requests
import request
import json
import pymysql
import datetime
import pandas as pd
import lxml,html5lib
from pandas import Series, DataFrame
import time
from headers import header
from getStockID import sid,name,market,coe


start = time.time()
starttime = int(time.strftime("%M", time.localtime()))
yesterday = datetime.datetime.now().strftime("%Y%m%d")

l = 0
for l in range(len(sid)):
    try:
        db = pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='Listing',
                         charset='utf8')
    except:
        pass
    cursor = db.cursor()
    asid = sid[l]
    aname = name[l]
    amarket = market[l]
    acoe = coe[l]

    params = {"date": yesterday,
              "stockNo": asid}
    conntime = b = int(time.strftime("%M", time.localtime()))
    proxiesList = ["http://60.249.6.104:8080", "http://60.249.6.105:8080",
                   "http://60.249.6.104:8080", "http://192.168.1.3:8080","http://192.168.2.12:8080","http://140.168.80.254:8080"] * 1000
    if conntime - starttime >= 1:
        headers = {'user-agent': header[l]}
        proxies = {'proxy': proxiesList[l]}
    else:  # 找可用IP塞到list
        headers = {'user-agent': "my-app/0.0.1"}
        proxies = {'proxy': "http://192.168.2.12:8080"}
    time.sleep(3)
    try:
        res = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY',
                       params=params, headers=headers, proxies=proxies)
        allData = json.loads(res.text)
    except:
        pass
    if ('data' in allData.keys()):
        _data = allData['data']
        select = (
            '''SELECT * FROM `stockdata` WHERE `date` = "''' + _data[-1][0] + '''" and `sid`="''' + asid + '''"''' )
        cursor.execute(select)
        row = cursor.fetchone()
        if row is not None:
            print row
        else:
            print 'none'

        db.commit()
    print asid + 'inserted'
    db.close()
end = time.time()
print end - start
#        select = (
#            '''SELECT * FROM `stockdata` WHERE `date` = "''' + _data[-1][0] + '''" and `sid`="''' + asid + '''"''' )
