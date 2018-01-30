# -*- coding: UTF-8_general_ci -*-
#上傳這個月個股資料到stockdata資料表
import requests
import request
import json
import pymysql
import datetime
import pandas as pd
import lxml,html5lib
from pandas import Series, DataFrame
import time
from getStockID import sid,name,market,coe
from headers import header


start = time.time()
starttime = int(time.strftime("%M", time.localtime()))
yesterday = datetime.datetime.now().strftime("%Y%m%d")

l = 0
for l in range(len(sid)):
    print l
    db = pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='Listing',
                         charset='utf8')
    cursor = db.cursor()
    asid = sid[l]
    aname = name[l]
    amarket = market[l]
    acoe = coe[l]
    print acoe
    print amarket
    print aname
    print asid
    #alter = """ALTER TABLE `"""+asid+"""` ADD `market` VARCHAR(50) NOT NULL AFTER `name`, ADD `coe` VARCHAR(50) NOT NULL AFTER `market`"""
    # cursor.execute(alter)
    params = {"date": 20171130,
              "stockNo": asid}
    conntime = b = int(time.strftime("%M", time.localtime()))
    proxiesList = ["http://60.249.6.104:8080", "http://60.249.6.105:8080",
                   "http://60.249.6.104:8080", "http://192.168.1.3:8080"] * 1000
    if conntime - starttime >= 1:
        headers = {'user-agent': header[l]}
        proxies = {'proxy': proxiesList[l]}
    else:  # 找可用IP塞到list
        headers = {'user-agent': "m y-app/0.0.1"}
        proxies = {'proxy': "http://60.249.6.105:8080"}
    time.sleep(2)
    try:
        res = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY',
                          params=params, headers=headers, proxies=proxies)
        allData = json.loads(res.text)
    except:
        pass;
    if ('data' in allData.keys()):
        _data = allData['data']
        for i in range(len(_data)):
            st = _data[i][1].encode('utf-8').replace(',', '')
            to = _data[i][2].encode('utf-8').replace(',', '')
            open = _data[i][3].encode('utf-8').replace(',', '')
            high = _data[i][4].encode('utf-8').replace(',', '')
            low = _data[i][5].encode('utf-8').replace(',', '')
            closing = _data[i][6].encode('utf-8').replace(',', '')
            tv = _data[i][8].encode('utf-8').replace(',', '')
            if str(open) == '--':
                open = 0.00
                high = 0.00
                low = 0.00
                closing = 0.00
            else:
                open = open
                high = high
                low = low
                closing = closing
            select = (
                '''SELECT * FROM `stockdata` WHERE `date` = "''' + _data[i][0] + '''" and `sid`="''' + asid + '''"''')
            cursor.execute(select)
            search = cursor.fetchone()
            if search is not None:
                pass
            else:
                insert = (
                    """INSERT  INTO `stockdata` (`date`, `sid`, `name`,`market`,`coe`, `shareTrades`, `turnover`, `open`, `high`, `low`, `closing`,`grossspread`,`tradingvolume`,`time`) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)""")
                da = (
                    _data[i][0], asid, aname, amarket, acoe, float(st), float(to), float(open), float(high),
                    float(low),
                    float(closing),
                    _data[i][7], float(tv), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                cursor.execute(insert, da)
                db.commit()
    print asid + 'inserted'
    db.close()
end = time.time()
print end - start