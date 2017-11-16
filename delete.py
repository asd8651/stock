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
    insert = (
        """delete from  `""" + sid + """`;""")
    cursor.execute(insert)
    print('Success increased---' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    db.commit()
    time.sleep(0.3)
db.close()
end=time.time()
print(end-start)