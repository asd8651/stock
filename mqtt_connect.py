import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("PV 702")

def on_message(client, userdata, msg):
    topic = "PV 702"
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("apecpv.cmru.ac.th", 1883, 60)
client.loop_forever()