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
from addStockId import mname,msid,mmarket,mcoe
from headers import header
import datetime

if datetime.date.today().weekday() == 5:
    print 'not time'
    time.sleep(86500)
elif datetime.date.today().weekday() == 6:
    print 'not time'
    time.sleep(60)
else:
    if int(time.strftime("%H%M", time.localtime())) == 1500:  # 若時間在9點~2點半
        starttime = int(time.strftime("%M", time.localtime()))
        yesterday = datetime.datetime.now().strftime("%Y%m%d")
        l = 0
        for l in range(len(msid)):
            db = pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='Listing',
                                 charset='utf8')  # 連接資料庫
            cursor = db.cursor()
            asid = msid[l]
            name = mname[l]
            market = mmarket[l]
            coe = mcoe[l]
            params = {"date": yesterday,
                      "stockNo": asid}
            conntime = b = int(time.strftime("%M", time.localtime()))
            proxiesList = ["http://60.249.6.104:8080", "http://60.249.6.105:8080",
                           "http://60.249.6.104:8080", "http://192.168.1.3:8080"] * 1000
            if (conntime - starttime >= 1):  # 若間隔2~3分鐘則換headers proxies
                headers = {'user-agent': header[l]}
                proxies = {'proxy': proxiesList[l]}
            else:  # 找可用IP塞到list
                headers = {'user-agent': "my-app/0.0.1"}
                proxies = {'proxy': "http://192.168.1.3:8080"}
            res = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY',
                               params=params, headers=headers, proxies=proxies)  # 爬API
            try:
                allData = json.loads(res.text)  # 改json格式，若失敗就pass
            except:
                pass;
            if ('data' in allData.keys()):  # 若抓到的json有data這個key
                _data = allData['data']
                insert = (
                    """INSERT  INTO `""" + asid + """` (`Date`, `sid`, `name`,`market`,`coe`, `shareTrades`, `turnover`, `open`, `high`, `low`, `closing`,`grossspread`,`tradingvolume`,`time`) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)""")
                da = (
                    _data[-1][0], asid, name, market, coe, _data[-1][1], _data[-1][2], _data[-1][3], _data[-1][4],
                    _data[-1][5],
                    _data[-1][6],
                    _data[-1][7], _data[-1][8], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                cursor.execute(insert, da)  # 新增資料，值
                try:
                    db.commit()
                except:
                    pass
                print asid + 'inserted'
            db.close()
    else:
        print 'not time'