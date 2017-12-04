# -*- coding: UTF-8_general_ci -*-
#上傳個股個股月營收到月營收資料表
#更新到106.11月

import requests
import request
import json
import pymysql
import datetime
import pandas as pd
import lxml,html5lib
from pandas import Series, DataFrame
import time
from getStockID import coe
from headers import header
now = datetime.datetime.now().strftime("%Y")
for year in range(102,int(now)-1911):
    # 假如是西元，轉成民國
    db = pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='Listing',
                         charset='utf8')#連資料庫
    cursor = db.cursor()
    for month in range(1,13):#月份
        print month
        # 下載該年月的網站，並用pandas轉換成 dataframe
        time.sleep(1)
        html_df = pd.read_html(
            'http://mops.twse.com.tw/nas/t21/sii/t21sc03_' + str(year) + '_' + str(month) + '_0.html')
        df = html_df[0].copy()
        df = df[list(range(0, 10))]
        column_index = df.index[(df[0] == u'公司代號')][0]
        df.columns = df.iloc[column_index]
        df[u'當月營收'] = pd.to_numeric(df[u'當月營收'], 'coerce')
        df = df[~df[u'當月營收'].isnull()]
        df = df[df[u'公司代號'] != u'合計']
        df = df.reset_index()
        #df為抓到的dataframe
        for q in range(len(df[u'公司代號'])):
            print year
            sid = df[u'公司代號'][q]
            name = df[u'公司名稱'][q]
            thisMonth = df[u'當月營收'][q]
            lastMonth = df[u'上月營收'][q]
            sametimeLastyear = df[u'去年當月營收'][q]
            compareLastmonth = df[u'上月比較增減(%)'][q]
            compareLastyear = df[u'去年同月增減(%)'][q]
            accumulation = df[u'當月累計營收'][q]
            accumulationLastyear = df[u'去年累計營收'][q]
            compareAccumulation = df[u'前期比較增減(%)'][q]
            if lastMonth == u'不適用':
                lastMonth = u'0'
                compareLastmonth = u'0'
            else:
                lastMonth = lastMonth
                compareLastmonth = compareLastmonth
            nanb = [sid,name,thisMonth,lastMonth,sametimeLastyear,compareLastmonth,compareLastyear,accumulation,accumulationLastyear,compareAccumulation]
            for s in range(len(nanb)):
                if type(nanb[s]) != type(nanb[1]):
                    if type(nanb[s]) != type(nanb[2]):
                        nanb[s] = 0
                    else:
                        nanb[s] = nanb[s]
            print nanb
            insert = (
                """INSERT INTO `Monthrevenue`( `sid`, `name`,`year`, `month`, `thisMonth`, `lastMonth`, `sametimeLastyear`,
                           `compareLastmonth`, `compareLastyear`, `accumulation`, `accumulationLastyear`, `compareAccumulation`,`date`) VALUES(%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s);""")
            da = (nanb[0], nanb[1], year, month, float(nanb[2]), float(nanb[3]), float(nanb[4]),
                  float(nanb[5]), float(nanb[6]), float(nanb[7]), float(nanb[8]),
                  float(nanb[9]), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            cursor.execute(insert, da)
            db.commit()
        print 'inserted'
    db.close()