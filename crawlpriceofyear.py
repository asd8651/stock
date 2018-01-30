# -*- coding: UTF-8_general_ci -*-
#上傳個股年資料
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
    params = {"stockNo": asid}
    conntime = int(time.strftime("%M", time.localtime()))
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
        res = requests.get('http://www.twse.com.tw/exchangeReport/FMNPTK',
                       params=params, headers=headers, proxies=proxies)
        allData = json.loads(res.text)
    except:
        pass;
    if ('data' in allData.keys()):
        _data = allData['data']
        _data2 = allData['data2']
        for i in range(len(_data)):
            year = _data[i][0]
            tradedshares = _data[i][1].encode('utf-8').replace(',', '')
            turnover = _data[i][2].encode('utf-8').replace(',', '')
            strokecount = _data[i][3].encode('utf-8').replace(',', '')
            high = _data[i][4].encode('utf-8').replace(',', '')
            highdate = _data[i][5]
            low = _data[i][6].encode('utf-8').replace(',', '')
            lowdate = _data[i][7]
            closing = _data[i][8].encode('utf-8').replace(',', '')
            recentyearhigh = _data2[0][0].encode('utf-8').replace(',', '')
            recentyearshighdate = _data2[0][1]
            recentyearlow = _data2[0][2].encode('utf-8').replace(',', '')
            recentyearslowdate = _data2[0][3]
            select = (
                '''SELECT * FROM `yeardata` WHERE `year` = "''' + str(_data[i][0]) + '''" and `sid`="''' + str(asid) + '''"''')
            cursor.execute(select)
            search = cursor.fetchone()
            if search is not None:
                print year
                print asid + 'excited'
            else:
                insert = (
                    """INSERT  INTO `yeardata` (`year`, `sid`, `name`,`tradedshares`,`turnover`, `strokecount`, `high`, `highdate`, `low`, `lowdate`, `closing`,`recentyearhigh`,`recentyearshighdate`,`recentyearlow`,`recentyearslowdate`,`date`) VALUES (%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)""")
                da = (
                year, asid, aname, float(tradedshares), float(turnover), float(strokecount), float(high), highdate,
                float(low),
                lowdate,
                float(closing),
                float(recentyearhigh), recentyearshighdate, float(recentyearlow), recentyearslowdate,
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                cursor.execute(insert, da)
                db.commit()
        print asid + 'inserted'
db.close()
end = time.time()
print end - start