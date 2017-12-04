# -*- coding: UTF-8_general_ci -*-
#上傳大盤即時資料到bigrealtime資料表
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


start = time.time()
starttime = int(time.strftime("%M", time.localtime()))
try:
    db = pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='Listing',
                         charset='utf8')
except:
    pass
cursor = db.cursor()

proxiesList = ["http://60.249.6.104:8080", "http://60.249.6.105:8080",
                "http://60.249.6.104:8080", "http://192.168.1.3:8080","http://192.168.2.12:8080"
                  , "http://140.168.80.254:8080"] * 10000
for l in range(16200):
    conntime = int(time.strftime("%M", time.localtime()))
    if conntime - starttime >= 1:
        headers = {'user-agent': header[l]}
        proxies = {'proxy': proxiesList[l]}
    else:  # 找可用IP塞到list
        headers = {'user-agent': "my-app/0.0.1"}
        proxies = {'proxy': "http://192.168.2.12:8080"}
    s=time.time()
    res = requests.get('http://mis.twse.com.tw/stock/api/getChartOhlcStatis.jsp?ex=tse&ch=t00.tw&fqy=1',
                       headers=headers, proxies=proxies)
    try:
        bigReattimeData = json.loads(res.text)
    except:
        pass;
    print bigReattimeData[u'ohlcArray'][-1][u's']
    cursor.execute("""SELECT `s` FROM `bigrealtime` order by `ID` DESC LIMIT 1""")
    last = cursor.fetchall()
    last = last.__str__()
    last = last.strip('()')
    last = last.replace('(', '')
    last = last.replace(')', '')
    last = last.replace(',', '')
    last = last.replace('u', '')
    last = last.replace("'", '')
    if bigReattimeData[u'ohlcArray'][-1][u's'] == last:
        pass
    else:
        if (u'ohlcArray' in bigReattimeData.keys()):
            _data = bigReattimeData[u'ohlcArray']
            insert = (
                """INSERT  INTO `bigrealtime` (`totalsecond`,`s`,`time`,`price`,`date`) VALUES (%s,%s,%s,%s,%s)""")
            da = (
                _data[-1]['t'], _data[-1]['s'], _data[-1]['ts'], _data[-1]['c'],
                datetime.datetime.now().strftime("%Y%m%d"))
            cursor.execute(insert, da)
            try:
                db.commit()
            except:
                pass
        print 'inserted'
    time.sleep(3)
    end = time.time()
    print end-s
    print end - start
db.close()
