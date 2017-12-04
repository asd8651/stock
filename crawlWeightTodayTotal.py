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
#上傳今天大盤盤後資訊到bigmarket

start = time.time()
yesterday = datetime.datetime.now().strftime("%Y%m%d")
starttime = int(time.strftime("%M", time.localtime()))
todaywdb = pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='Listing',
                                 charset='utf8')
cursor = todaywdb.cursor()
params = {"date":yesterday }
headers = {'user-agent': "my-app/0.0.1"}
proxies = {'proxy': "http://192.168.1.3:8080"}
res = requests.get('http://www.twse.com.tw/exchangeReport/FMTQIK',
                   params=params, headers=headers, proxies=proxies)
try:
    bigData = json.loads(res.text)
except:
    pass;
cursor.execute("""SELECT `date` FROM `bigmarket` order by `ID` DESC LIMIT 1""")
last = cursor.fetchall()
last = last.__str__()
last = last.strip('()')
last = last.replace('(', '')
last = last.replace(')', '')
last = last.replace(',', '')
last = last.replace('u', '')
last = last.replace("'", '')#改為字串
if bigData[u'data'][-1][0] == last:
    pass
else:
    if (u'data' in bigData.keys()):
        _data = bigData[u'data']
        insert = (
             """INSERT  INTO `bigmarket` (`date`, `tradedshares`, `turnover`,`strokecount`,`price`,`changerange`,`time`) VALUES (%s,%s,%s,%s,%s, %s, %s)""")
        da = (
            _data[-1][0], _data[-1][1], _data[-1][2], _data[-1][3], _data[-1][4], _data[-1][5],
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute(insert, da)
        todaywdb.commit()
        print _data[-1][0] + 'inserted'
    else:
        print 'todayweight insert not yet'
    todaywdb.close()
end = time.time()
print end - start