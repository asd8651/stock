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
month = [19920128,19920228,19920328,19920428,19920528,19920628,19920728,19920828,19920928,19921028,19921128,19921228,
19930128,19930228,19930328,19930428,19930528,19930628,19930728,19930828,19930928,19931028,19931128,19931228,
19940128,19940228,19940328,19940428,19940528,19940628,19940728,19940828,19940928,19941028,19941128,19941228,
19950128,19950228,19950328,19950428,19950528,19950628,19950728,19950828,19950928,19951028,19951128,19951228,
19960128,19960228,19960328,19960428,19960528,19960628,19960728,19960828,19960928,19961028,19961128,19961228,
19970128,19970228,19970328,19970428,19970528,19970628,19970728,19970828,19970928,19971028,19971128,19971228,
19980128,19980228,19980328,19980428,19980528,19980628,19980728,19980828,19980928,19981028,19981128,19981228,
19990128,19990228,19990328,19990428,19990528,19990628,19990728,19990828,19990928,19991028,19991128,19991228,
20000128,20000228,20000328,20000428,20000528,20000628,20000728,20000828,20000928,20001028,20001128,20001228,
20010128,20010228,20010328,20010428,20010528,20010628,20010728,20010828,20010928,20011028,20011128,20011228,
20020128,20020228,20020328,20020428,20020528,20020628,20020728,20020828,20020928,20021028,20021128,20021228,
20030128,20030228,20030328,20030428,20030528,20030628,20030728,20030828,20030928,20031028,20031128,20031228,
20040128,20040228,20040328,20040428,20040528,20040628,20040728,20040828,20040928,20041028,20041128,20041228,
20050128,20050228,20050328,20050428,20050528,20050628,20050728,20050828,20050928,20051028,20051128,20051228,
20060128,20060228,20060328,20060428,20060528,20060628,20060728,20060828,20060928,20061028,20061128,20061228,
20070128,20070228,20070328,20070428,20070528,20070628,20070728,20070828,20070928,20071028,20071128,20071228,
20080128,20080228,20080328,20080428,20080528,20080628,20080728,20080828,20080928,20081028,20081128,20081228,
20090128,20090228,20090328,20090428,20090528,20090628,20090728,20090828,20090928,20091028,20091128,20091228,
20100128,20100228,20100328,20100428,20100528,20100628,20100728,20100828,20100928,20101028,20101128,20101228,
20110128,20110228,20110328,20110428,20110528,20110628,20110728,20110828,20110928,20111028,20111128,20111228,
20120128,20120228,20120328,20120428,20120528,20120628,20120728,20120828,20120928,20121028,20121128,20121228,
20130128,20130228,20130328,20130428,20130528,20130628,20130728,20130828,20130928,20131028,20131128,20131228,
20140128,20140228,20140328,20140428,20140528,20140628,20140728,20140828,20140928,20141028,20141128,20141228,
20150128,20150228,20150328,20150428,20150528,20150628,20150728,20150828,20150928,20151028,20151128,20151228,
20160128,20160228,20160328,20160428,20160528,20160628,20160728,20160828,20160928,20161028,20161128,20161228,
20170128,20170228,20171205]
l = 0
for mon in range(len(month)):
    for l in range(len(sid)):
        print l
        db = pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='Listing',
                             charset='utf8')
        cursor = db.cursor()
        asid = sid[l]
        aname = name[l]
        amarket = market[l]
        acoe = coe[l]
        params = {"date": month[mon],
                  "stockNo": asid}
        conntime = b = int(time.strftime("%M", time.localtime()))
        proxiesList = ["http://60.249.6.104:8080", "http://60.249.6.105:8080",
                       "http://60.249.6.104:8080", "http://192.168.1.3:8080"] * 1000
        if conntime - starttime >= 1:
            headers = {'user-agent': header[l]}
            proxies = {'proxy': proxiesList[l]}
        else:  # 找可用IP塞到list
            headers = {'user-agent': "my-app/0.0.1"}
            proxies = {'proxy': "http://60.249.6.105:8080"}
        time.sleep(2)
        try:
            res = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY',
                                params=params, headers=headers, proxies=proxies)
            allData = json.loads(res.text)
        except:
            pass
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
                    print _data[i][0]
                    print asid+'excited'
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