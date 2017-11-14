import paho.mqtt.client as mqtt
import requests
import time
import json
import sys
import pymysql
db =pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='projectiot' , charset='utf8')
cursor = db.cursor()
params = {"code": data['pv_volt'], "name": data['pv_cur'], "capacity": data['pv_power'],
              "open": data['Rediation'], "high": data['pv_Temp'], "low": data['amb_temp'],
              "closing": data['Daily'], "category": data['total_L'], "date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
res = requests.post('http://60.249.6.104:8787/api/store/MMeZwZMbHIDa', params=params)
print(res.text)
cursor.execute("""SELECT id FROM `fields` WHERE id>=35""")
searchID = cursor.fetchall()
for i in range(10):
    insert = ("""INSERT INTO `data` (`field_id`, `value`, `time`) VALUES(%s,%s,%s)""")
    da = (searchID[i], 'd' + str(i), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cursor.execute(insert, da)
db.commit()
