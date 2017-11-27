# -*- coding: UTF-8_unicode_ci -*-
import pymysql
import time
#import twstock
db =pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='onmarket' , charset='utf8')
cursor = db.cursor()
cursor.execute("""SELECT sid FROM `stockID`""")
searchID = cursor.fetchall()

#get execute data(list)
sid=searchID
codeList=[]
for i in range(len(sid)):
    sid = searchID.__str__()
    sid = sid.strip('()')
    sid = sid.replace('(', '')
    sid = sid.replace(')', '')
    sid = sid.replace(',', '')
    sid = sid.replace('u', '')
    sid = sid.replace("'", '')
    sid = sid.split(' ')
    codeList.append(sid[i])