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
db = pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='Listing',
                                 charset='utf8')  # 連接資料庫
cursor = db.cursor()
cursor.execute("""SELECT `stockID` FROM `stockID`""")
sid=cursor.fetchall()
ssid = []
for roow in sid:
    q=0
    f = roow[q]
    f.encode('utf8')
    ssid.append(f)
    q = q + 1
print ssid[0]
cursor.execute("""SELECT `name` FROM `stockID`""")
name=cursor.fetchall()
sname = []
for row in name:
    i=0
    a = row[i]
    a.encode('utf8')
    sname.append(a)
    i = i + 1
print sname[0]
class toMysql(object):
    starttime = int(time.strftime("%M", time.localtime()))
    yesterday = datetime.datetime.now().strftime("%Y%m%d")
    start = time.time()
    proxiesList = ["http://60.249.6.104:8080", "http://60.249.6.105:8080",
                       "http://60.249.6.104:8080", "http://192.168.1.3:8080", "http://192.168.2.12:8080"] * 1000
    def todayPrice():#上傳今天個股資訊，要時間條件
        for l in range(len(msid)):
            todaypdb = pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='Listing',
                                 charset='utf8')  # 連接資料庫
            cursor = todaypdb.cursor()
            asid = msid[l]
            name = mname[l]
            market = mmarket[l]
            coe = mcoe[l]
            params = {"date": yesterday,
                      "stockNo": asid}
            conntime = int(time.strftime("%M", time.localtime()))
            if (conntime - starttime >= 1):  # 若間隔2~3分鐘則換headers proxies
                headers = {'user-agent': header[l]}
                proxies = {'proxy': proxiesList[l]}
            else:  # 找可用IP塞到list
                headers = {'user-agent': "my-app/0.0.1"}
                proxies = {'proxy': "http://60.249.6.105:8080"}
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
                print 'today'+asid+'inserted'
            db.close()

    def todayWeight():#上傳今天大盤資訊，可設無窮迴圈不必時間條件
        time.sleep(120)
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
                try:
                    db.commit()
                except:
                    pass
                print _data[-1][0] + 'inserted'
            else:
                print 'todayweight insert not yet'
            db.close()
    def realtimeWeight():#大盤即時，要設時間條件
        realwdb = pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='Listing',
                                 charset='utf8')
        cursor = realwdb.cursor()
        for l in range(16200):#16200 = 一天總秒數
            conntime = int(time.strftime("%M", time.localtime()))
            if conntime - starttime >= 1:
                headers = {'user-agent': header[l]}
                proxies = {'proxy': proxiesList[l]}
            else:  # 找可用IP塞到list
                headers = {'user-agent': "my-app/0.0.1"}
                proxies = {'proxy': "http://192.168.1.3:8080"}
            s = time.time()
            res = requests.get('http://mis.twse.com.tw/stock/api/getChartOhlcStatis.jsp?ex=tse&ch=t00.tw&fqy=1',
                               headers=headers, proxies=proxies)
            try:
                weightreal = json.loads(res.text)
            except:
                pass;
            cursor.execute("""SELECT `s` FROM `bigrealtime` order by `ID` DESC LIMIT 1""")
            last = cursor.fetchall()
            last = last.__str__()
            last = last.strip('()')
            last = last.replace('(', '')
            last = last.replace(')', '')
            last = last.replace(',', '')
            last = last.replace('u', '')
            last = last.replace("'", '')
            cursor.execute("""SELECT `time` FROM `bigrealtime` order by `ID` DESC LIMIT 1""")
            sqlt = cursor.fetchall()
            sqlt = sqlt.__str__()
            sqlt = sqlt.strip('()')
            sqlt = sqlt.replace('(', '')
            sqlt = sqlt.replace(')', '')
            sqlt = sqlt.replace(',', '')
            sqlt = sqlt.replace('u', '')
            sqlt = sqlt.replace("'", '')
            if weightreal[u'ohlcArray'][-1][u's'] == last:
                pass;
            elif weightreal[u'ohlcArray'][-1][u'ts'] == sqlt:
                pass
            else:
                if (u'ohlcArray' in weightreal.keys()):
                    _data = weightreal[u'ohlcArray']
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
                    print weightreal[u'ohlcArray'][-1][u'ts']+'inserted'
            time.sleep(1)
            end = time.time()
            print end - s
            print end - start
        db.close()
To = toMysql()
To.todayWeight()
'''
if datetime.date.today().weekday() == 5:
    print 'not time'
    time.sleep(86500)
elif datetime.date.today().weekday() == 6:
    print 'not time'
    time.sleep(60)
else:
    if int(time.strftime("%H%M", time.localtime())) >= 1530:  # 若時間在9點~2點半
    else:
        print 'not time'
'''
TypeError: todayWeight() takes no arguments (1 given)