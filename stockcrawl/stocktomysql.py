import requests
import time
import json
import sys
import pymysql
import pandas as pd
from getStockID import codeList#codeList:stock id
import twstock
start=time.time()
db =pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='stockdata' , charset='utf8')
cursor = db.cursor()
#while True:
w = 0
for w in range(len(codeList)):
    sid = codeList[w]
    category = twstock.codes[sid].market
    name = twstock.codes[sid].name
    print(sid)
    try:
        capacity = twstock.realtime.get(sid)['realtime']['trade_volume']
        open = twstock.realtime.get(sid)['realtime']['open']
        close = twstock.realtime.get(sid)['realtime']['latest_trade_price']
        high = twstock.realtime.get(sid)['realtime']['high']
        low = twstock.realtime.get(sid)['realtime']['low']
        date = twstock.realtime.get(sid)['info']['time']
    except KeyError:
        pass
    print(close)
    insert = (
        """INSERT  INTO `""" + sid + """` (`code`, `name`, `capacity`, `open`, `high`, `low`, `closing`, `category`, `date`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""")
    da = (sid, name, capacity, open, high, low, close, category, date)
    cursor.execute(insert, da)

    print('Success increased'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    db.commit()
db.close()
end=time.time()
print(end-start)