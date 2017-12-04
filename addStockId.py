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
#抓取上市股票代碼名稱－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
df=pd.read_html('http://isin.twse.com.tw/isin/C_public.jsp?strMode=2',encoding='big5hkscs',header=0)
#http://isin.twse.com.tw/isin/C_public.jsp?strMode=2 上市  4:上櫃
newdf=df[0][df[0][u'產業別'] > '0']
del newdf[u'國際證券辨識號碼(ISIN Code)'],newdf[u'CFICode'],newdf[u'備註']
df2=newdf[u'有價證券代號及名稱'].str.split(' ', expand=True)
df2 = df2.reset_index(drop=True)
newdf = newdf.reset_index(drop=True)
for i in df2.index:
    if u'　' in df2.iat[i,0]:
        df2.iat[i,1]=df2.iat[i,0].split(u'　')[1]
        df2.iat[i,0]=df2.iat[i,0].split(u'　')[0]
newdf=df2.join(newdf)
newdf=newdf.rename(columns = {0:u'股票代號',1:u'股票名稱'})
del newdf[u'有價證券代號及名稱'],newdf[u'上市日']
msid = newdf[u'股票代號']
mname = newdf[u'股票名稱']
mmarket = newdf[u'市場別']
mcoe = newdf[u'產業別']
print msid

if __name__ == "__main__":
    db = pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='Listing', charset='utf8')
    cursor = db.cursor()
    l = 0
    for l in range(len(msid)):
        yesterday = datetime.datetime.now().strftime("%Y%m%d")
        sid = msid[l]
        name = mname[l]
        market = mmarket[l]
        coe = mcoe[l]
        insertSID = (
            """INSERT  INTO `stockID` (`stockID`,`name`,`market`,`coe`,`date`) VALUES (%s,%s,%s, %s, %s)""")
        da = (sid, name,market,coe, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute(insertSID, da)
        db.commit()
    print 'complete'
    db.close()

