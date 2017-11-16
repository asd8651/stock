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
    print sid+u'有資料喔';
    if ('data' in allData.keys()):
        print 'data exists';
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
                        closing varchar(30))
                        ENGINE = InnoDB,
                        CHARSET=utf8,
                        COLLATE utf8_unicode_ci;"""
        cursor.execute(sql)
        for i in range(len(_data)):
            insert = ("""INSERT  INTO `""" + sid + """` (`Date`, `sid`, `name`, `shareTrades`, `turnover`, `open`, `high`, `low`, `closing`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""")
            # ON DUPLICATE KEY UPDATE (`Date`,`sid`,`name`,`shareTrades`,`turnover`,`over`,`high`,`low`,`closing`)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)有更新，無新增
            da = (_data[i][0], sid, name, _data[i][1], _data[i][2], _data[i][3], _data[i][4], _data[i][5], _data[i][6])
            cursor.execute(insert,da)
            db.commit()
        delete = """delete from `""" + sid + """` where date in (select date from `""" + sid + """` group by date having count(*)>1) and ID not in (select min(ID) from `""" + sid + """` group by date having count(*)>1)"""
        cursor.execute(delete)
        db.commit()
    time.sleep(2)
db.close()
end=time.time()
print end-start
#引入thread 同時上傳上市上貴資料