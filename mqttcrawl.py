import paho.mqtt.client as mqtt
import requests
import time
import json
import sys
import pymysql
db =pymysql.connect(host='60.249.6.104', port=33060, user='root', passwd='ncutim', db='projectiot' , charset='utf8')
cursor = db.cursor()
def on_connect(mqttc, obj, flags, rc):
    pass
def on_message(mqttc, obj, msg):
    time.sleep(1)
    #print(msg.payload=="pv702\n")
    if(msg.payload!="pv702\n"):
        time.sleep(1)
    #try:
        data = json.loads(msg.payload)
        print data
        params = {"pv_volt": data['pv_volt'], "pv_cur": data['pv_cur'], "pv_power": data['pv_power'],"Rediation": data['Rediation'],"pv_Temp": data['pv_Temp'],"amb_temp": data['amb_temp'],"Daily": data['Daily'],"total_L": data['total_L'],"total_H": data['total_H'], "time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        res = requests.post('http://60.249.6.104:8787/api/store/MMeZwZMbHIDa', params=params)
        print res.text
        cursor.execute("""SELECT id FROM `fields` WHERE id>=35""")
        searchID = cursor.fetchall()
        d0 = data['pv_volt']
        d1 = data['pv_cur']
        d2 = data['pv_power']
        d3 = data['Rediation']
        d4 = data['pv_Temp']
        d5 = data['amb_temp']
        d6 = data['Daily']
        d7 = data['total_L']
        d8 = data['total_H']
        d9 = data['pv_volt']
        if (searchID):
            print 'nice'
        for i in range(10):
            insert = ("""INSERT  INTO `data` (`field_id`, `value`, `time`) VALUES (%s, %s, %s)""")
            da = (searchID[i],'d'+str(i),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            cursor.execute(insert, da)
            db.commit()
def on_publish(mqttc, obj, mid):
    pass
def on_subscribe(mqttc, obj, mid, granted_qos):
    pass
def on_log(mqttc, obj, level, string):
    pass
mqttc = mqtt.Client(client_id="ncut_user6537374555")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.username_pw_set(username="admin", password="admin")
mqttc.connect("apecpv.cmru.ac.th", 1883, 60)
mqttc.subscribe("pv702", 0)
mqttc.loop_forever()