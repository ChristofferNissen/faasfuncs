import base64
from typing import NamedTuple
import datetime
import json
import os

import paho.mqtt.client as mqtt
import requests

MQTT_ADDRESS = 'influx.itu.dk'
MQTT_PORT = 8883
MQTT_USER = 'smartreader'
MQTT_PASSWORD = os.getenv('mqtt-pass')
MQTT_TOPIC = 'IoT2020sec/meters'
MQTT_CAPATH = './certs/ca-certificates.crt'

#4mp3r3h0ur

topic_name=MQTT_TOPIC
# gateway_url=MQTT_ADDRESS
# topic_name = os.getenv("topic", "sensor-readings")
gateway_url = os.getenv("gateway_url", "https://gateway.christoffernissen.me")


print("Using gateway {} and topic {}".format(gateway_url, topic_name))

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_name)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    data = {
        'data': str(msg.payload),
        'created_at': str(datetime.datetime.now())
    }
    r = json.dumps(data)
    
    print("r", r)
    
    with open("./samples.txt", "a") as f:
        f.write(r + "\n")
        f.close()

    print(msg.topic+" "+json.dumps(r))

    res = requests.post(gateway_url + "/function/iot-assignment2", data=r)
    print("Log reading with function: ", res.status_code)

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqtt_client.tls_set(MQTT_CAPATH)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_ADDRESS, MQTT_PORT, 60)
mqtt_client.loop_forever()