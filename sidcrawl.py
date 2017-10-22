# -*- coding: UTF-8_general_ci -*-

import requests
import request
import json
import pymysql
import datetime
import pandas as pd
import lxml,html5lib
from pandas import Series, DataFrame

yesterday = datetime.datetime.now().strftime("%Y%m%d")
params = {"date": yesterday,
          "stockNo":"2330"}
res = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY',
                     params=params)
allData = json.loads(res.text)
#fields = json.dumps(fie, encoding="UTF-8", ensure_ascii=False) �ഫ��str
today = allData['data'][-1]
date = str(today[0])
open = today[3]
high = today[4]
low = today[5]
closing = today[6]
shareTrades = today[1]
turnover = today[2]
dataDict = {'date' : date,'open': open,'high': high,'low':low,'closing':closing,'shareTrades':shareTrades,'turnover':turnover}
#print type(data)�s�X����
db = pymysql.connect("localhost","root","asd865100","stock",charset="utf8")
cursor = db.cursor()
#�s�W
insert = ("INSERT ignore  INTO stockdata (`Date`, `sid`, `name`, `shareTrades`, `turnover`, `open`, `high`, `low`, `closing`)"
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
data = (date, '2330','�x�n�q',shareTrades,turnover,open,high,low,closing)
'''try:
    # sql = "DELE TE FROM `stockData` WHERE sid = '2344'"# �R��
    # cursor.execute(sql)
    cursor.execute(insert, data)
    db.commit()
except:
    print "error"
'''
#��Ѳ��N����}�C��for�j��
#����W���d�Ѳ��N�X�W�١ССССССССССССССССССССССССССССССССССССС�
    #�W��
df=pd.read_html('http://isin.twse.com.tw/isin/C_public.jsp?strMode=2',encoding='big5hkscs',header=0)
newdf=df[0][df[0][u'���~�O'] > '0']
del newdf[u'����Ҩ���Ѹ��X(ISIN Code)'],newdf[u'CFICode'],newdf[u'�Ƶ�']
df2=newdf[u'�����Ҩ�N���ΦW��'].str.split(' ', expand=True)
df2 = df2.reset_index(drop=True)
newdf = newdf.reset_index(drop=True)
for i in df2.index:
    if u'�@' in df2.iat[i,0]:
        df2.iat[i,1]=df2.iat[i,0].split(u'�@')[1]
        df2.iat[i,0]=df2.iat[i,0].split(u'�@')[0]
newdf=df2.join(newdf)
newdf=newdf.rename(columns = {0:u'�Ѳ��N��',1:u'�Ѳ��W��'})
del newdf[u'�����Ҩ�N���ΦW��'],newdf[u'�W����']
    #�W�d
odf=pd.read_html('http://isin.twse.com.tw/isin/C_public.jsp?strMode=4',encoding='big5hkscs',header=0)
otcdf=odf[0][odf[0][u'���~�O'] > '0']
del otcdf[u'����Ҩ���Ѹ��X(ISIN Code)'],otcdf[u'CFICode'],otcdf[u'�Ƶ�']
odf2=otcdf[u'�����Ҩ�N���ΦW��'].str.split(' ', expand=True)
odf2 = odf2.reset_index(drop=True)
otcdf = otcdf.reset_index(drop=True)
for i in odf2.index:
    if u'�@' in odf2.iat[i,0]:
        odf2.iat[i,1]=odf2.iat[i,0].split(u'�@')[1]
        odf2.iat[i,0]=odf2.iat[i,0].split(u'�@')[0]
otcdf=odf2.join(otcdf)
otcdf=otcdf.rename(columns = {0:u'�Ѳ��N��',1:u'�Ѳ��W��'})
del otcdf[u'�����Ҩ�N���ΦW��'],otcdf[u'�W����']
print otcdf[u'�Ѳ��N��']
#�СССССССССССССССССССССССССССССССССССССССССССССССС�