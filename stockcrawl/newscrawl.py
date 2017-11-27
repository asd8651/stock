# -*- coding: UTF-8_general_ci -*-
import requests
from bs4 import BeautifulSoup

res = requests.get("https://news.google.com/news/explore/section/q/%E8%87%BA%E7%81%A3%E8%AD%89%E5%88%B8%E4%BA%A4%E6%98%93%E6%89%80/%E8%87%BA%E7%81%A3%E8%AD%89%E5%88%B8%E4%BA%A4%E6%98%93%E6%89%80?ned=tw&hl=zh-TW")
soup = BeautifulSoup(res.text,"html.parser")
#爬蟲常用的套件
count = 1

for item in soup.select(".nuEeue"):
    print ('======[',count,']=========')
    news_title = (item.text)
    news_url = item.get('href')
    print (news_title)#顯示新聞標題
    print (news_url)#顯示網址
    count += 1
