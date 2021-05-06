"""This script receives event data from MQTT by subscribing to a topic"""
import json
from paho.mqtt.client import Client as MqttClient
from os import getenv
from os import environ

from twitter_alert import send_tweet

def run():
    """Main method that obtains enviroment variables and connects to MQTT"""
    host = getenv("MQTT_HOST", "localhost")
    port = int(getenv("MQTT_PORT", 1883))
    username = getenv("MQTT_USERNAME", "")
    password = getenv("MQTT_PASSWORD", "")
    clientid = getenv("MQTT_CLIENTID", "events") + "_rec"

    client = create_client(host, port, username, password, clientid)

    client.loop_forever()


def create_client(host, port, username, password, clientid):
    """Creating an MQTT Client Object"""
    client = MqttClient(clientid)

    if username and password:
        client.username_pw_set(username=username, password=password)

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host=host, port=port)
    return client


def on_connect(client, userdata, flags, resultcode):
    """Upon connecting to an MQTT server, subscribe to the /traces topic"""
    print(f"✅ Connected with result code {resultcode}")

    region = getenv("MQTT_REGION", "")
    client.subscribe("iot-2/type/OpenEEW/id/" + region + "/evt/event/fmt/json")


def on_message(client, userdata, message):
    """When a message is sent to a subscribed topic,
    decode the message and send it to another method"""
    try:
        decoded_message = str(message.payload.decode("utf-8", "ignore"))
        data = json.loads(decoded_message)
        print(f"Received data: {data}")
        send_tweet("Testing") # Make up message later

    except BaseException as exception:
        print(exception)


run()
