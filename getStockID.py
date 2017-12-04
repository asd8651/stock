# -*- coding: UTF-8_unicode_ci -*-
import pymysql
import time
#取得股票代碼及名稱
db = pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='Listing',
                                 charset='utf8')  # 連接資料庫
cursor = db.cursor()
cursor.execute("""SELECT `stockID` FROM `stockID`""")
ssid=cursor.fetchall()
sid = []
for roow in ssid:
    q=0
    f = roow[q]
    f.encode('utf8')
    sid.append(f)
    q = q + 1
cursor.execute("""SELECT `name` FROM `stockID`""")
sname=cursor.fetchall()
name = []
for row in sname:
    i=0
    a = row[i]
    a.encode('utf8')
    name.append(a)
    i = i + 1
cursor.execute("""SELECT `market` FROM `stockID`""")
smarket=cursor.fetchall()
market = []
for rooow in smarket:
    d=0
    s = rooow[d]
    s.encode('utf8')
    market.append(s)
    d = d + 1
cursor.execute("""SELECT `coe` FROM `stockID`""")
scoe=cursor.fetchall()
coe = []
for rowrow in scoe:
    t=0
    g = rowrow[t]
    g.encode('utf8')
    coe.append(g)
    t = t + 1
if __name__=="__main__":
    print type(sid[0])
    print sid[0]
    print name[5]
    print market[0]
    print coe[0]
    print len(sid)
