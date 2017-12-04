# -*- coding: UTF-8-*-
import requests

from bs4 import BeautifulSoup
import pymysql
from headers import header
from ipproxies import proxiesList
import time
import datetime
#抓google新聞到news資料表
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
starttime = int(datetime.datetime.now().strftime("%M"))
for w in range(len(sname)):
    conntime = int(datetime.datetime.now().strftime("%M"))
    if (conntime - starttime >= 1):  # 若間隔2~3分鐘則換headers proxies
        headers = {'user-agent': header[w]}
        proxies = {'proxy': proxiesList[w]}
    else:  # 找可用IP塞到list
        headers = {'user-agent': "my-app/0.0.1"}
        proxies = {'proxy': "http://60.249.6.105:8080"}
    try:
        res = requests.get("https://news.google.com/news/search/section/q/"+sname[w]+"/"+sname[w]+"?hl=zh-TW",
                                    headers=headers, proxies=proxies)
    except:
        pass
    soup = BeautifulSoup(res.text, "html.parser")
    news_title=[]
    news_url=[]
    news_source=[]
    news_time = []
    for item in soup.select(".nuEeue"):#標題與網址
        newstitle = (item.text)
        newsurl = item.get('href')
        newstitle.encode('utf-8')
        newsurl.encode('utf-8')
        news_title.append(newstitle)
        news_url.append(newsurl)
    for source in soup.select(".IH8C7b"):#來源
        newssource = source.text
        newssource.encode('utf-8')
        news_source.append(newssource)
    for time in soup.select(".d5kXP"):#時間
        potime = time.text
        potime.encode('utf-8')
        news_time.append(potime)
    if news_title is not None:
        for b in range(len(news_time)):
            print news_title[b]
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert = (
                """INSERT  INTO `news` (`sid`,`name`,`title`,`url`,`source`,`date`,`addtime`) VALUES (%s,%s, %s, %s, %s, %s, %s)""")
            da = (ssid[w], sname[w], news_title[b], news_url[b], news_source[b], news_time[b], now)
            try:
                cursor.execute(insert, da)
                db.commit()
            except:
                pass
        print ssid[w] + 'insert'

db.close()