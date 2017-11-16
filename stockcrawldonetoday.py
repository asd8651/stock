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
from getStockID import codeList
from getStockID import sid
from getStockID import nameList
start=time.time()
yesterday = datetime.datetime.now().strftime("%Y%m%d")
#抓取上市櫃股票代碼名稱－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
db =pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='stock' , charset='utf8')
cursor = db.cursor()
if (db):
    print 'good';
l = 0
for l in range(len(sid)):
    sid = codeList[l]
    name = nameList[l]
    params = {"date": yesterday,
              "stockNo": sid}
    headers = {'user-agent': 'my-app/0.0.1'}
    res = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY',
                       params=params)
    allData = json.loads(res.text)
    print sid+u'有資料喔'
    if ('data' in allData.keys()):
        print 'data exists'
        _data = allData['data']
        sql = """CREATE TABLE IF NOT EXISTS `""" + sid + """`(
                        ID INT AUTO_INCREMENT PRIMARY KEY,
                        date  varchar(30) ,
                        sid varchar(20),
                        name varchar(20),  
                        shareTrades	varchar(30),
                        turnover varchar(30) ,
                        open varchar(30),
                        high varchar(30) ,
                        low varchar(30) ,
                        closing varchar(30),
                        time varchar(30))
                        ENGINE = InnoDB,
                        CHARSET=utf8,
                        COLLATE utf8_unicode_ci;"""
        cursor.execute(sql)
        insert = ("""INSERT  INTO `""" + sid + """` (`Date`, `sid`, `name`, `shareTrades`, `turnover`, `open`, `high`, `low`, `closing`,`time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)""")
        da = (_data[-1][0], sid, name, _data[-1][1], _data[-1][2], _data[-1][3], _data[-1][4], _data[-1][5], _data[-1][6], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute(insert,da)
        db.commit()
        print l
    time.sleep(2)
db.close()
end=time.time()
print end-start
#引入thread 同時上傳上市上貴資料