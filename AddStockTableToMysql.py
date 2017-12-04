# -*- coding: UTF-8_general_ci -*-
#新增個股資料表到Listing
import request
import json
import pymysql
import datetime
import pandas as pd
import lxml,html5lib
from pandas import Series, DataFrame
import time
from getStockID import sid,name,market,coe
start=time.time()
yesterday = datetime.datetime.now().strftime("%Y%m%d")

db =pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='Listing' , charset='utf8')
cursor = db.cursor()
l = 0
for l in range(len(sid)):
    asid = sid[l]
    name = name[l]
    params = {"date": yesterday,
              "stockNo": asid}
    time.sleep(2)
    sql = """CREATE TABLE IF NOT EXISTS `""" + asid + """`(
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
                                                grossspread varchar(100),
                                                tradingvolume varchar(100),
                                                time varchar(30))
                                                ENGINE = InnoDB,
                                                CHARSET=utf8,
                                                COLLATE utf8_unicode_ci;"""
    cursor.execute(sql)
    print asid + 'table created'
        # 找時間
    db.commit()
db.close()
end = time.time()
print end - start
    # 引入thread 同時上傳上市上貴資料