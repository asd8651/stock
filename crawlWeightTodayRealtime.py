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
from headers import header
#上傳今天大盤每五秒資料到bigrealtime

start = time.time()
starttime = int(time.strftime("%M", time.localtime()))
try:
        db = pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='Listing',
                         charset='utf8')
except:
    pass
cursor = db.cursor()

conntime = int(time.strftime("%M", time.localtime()))
proxiesList = ["http://60.249.6.104:8080", "http://60.249.6.105:8080",
                "http://60.249.6.104:8080", "http://192.168.1.3:8080"] * 1000

if conntime - starttime >= 1:
    headers = {'user-agent': header[l]}
    proxies = {'proxy': proxiesList[l]}
else:  # 找可用IP塞到list
    headers = {'user-agent': "my-app/0.0.1"}
    proxies = {'proxy': "http://192.168.1.3:8080"}

res = requests.get('http://mis.twse.com.tw/stock/api/getChartOhlcStatis.jsp?ex=tse&ch=t00.tw&fqy=1',
                   headers=headers, proxies=proxies)
try:
    bigReattimeData = json.loads(res.text)
except:
    pass;
print bigReattimeData[u'ohlcArray']
if (u'ohlcArray' in bigReattimeData.keys()):
    _data = bigReattimeData[u'ohlcArray']
    for i in range(len(_data)):
        insert = (
            """INSERT  INTO `bigrealtime` (`totalsecond`,`s`,`time`,`price`,`date`) VALUES (%s,%s,%s,%s,%s)""")
        da = (_data[i]['t'],_data[i]['s'],_data[i]['ts'],_data[i]['c'],datetime.datetime.now().strftime("%Y%m%d"))
        cursor.execute(insert, da)
        try:
            db.commit()
        except:
            pass
print 'inserted'
db.close()
end = time.time()
print end - start
