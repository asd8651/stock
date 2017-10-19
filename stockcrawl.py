# -*- coding: UTF-8_general_ci -*-

import requests
import json
import pymysql


db = pymysql.connect("localhost","root","asd865100","stock",charset="utf8")
cursor = db.cursor()

sql = """INSERT INTO `stockData` (`Date`, `sid`, `name`, `shareTrades`, `turnover`, `open`, `high`, `low`, `closing`, `volume`, `transaction`) VALUES ('2017-10-02', '2330', '台積電', '100000', '100', '213', '220', '210', '216', '123456789', '123456');"""
#新增
#sql = "DELETE FROM `stockData` WHERE sid = '2330'"; 刪除

try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()

params = {"date":"20171019",
          "stockNo":"2344"}
res = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY',
                     params=params)
print(res.text)