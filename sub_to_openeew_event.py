"""This script receives event data from MQTT by subscribing to a topic"""
import json
from os import getenv

from paho.mqtt.client import Client as MqttClient

from geopy.geocoders import Nominatim
from twitter_alert import send_tweet


def run():
    """Main method that obtains enviroment variables and connects to MQTT"""
    host = getenv("MQTT_HOST", "localhost")
    port = int(getenv("MQTT_PORT", "1883"))
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

        city = coordinates_to_city(data["lat"], data["lon"])

        twitter_msg = format_message(city, data["mag"])
        send_tweet(twitter_msg)

    except BaseException as exception:
        print(exception)


def format_message(city, magnitude):
    """Creates a twitter message using the city and magnitude"""
    short_slack_invite_url = "https://bit.ly/3u6Xji4"  # made on bitly, likely temporary
    event_msg = f"OpenEEW has detected an earthquake of magnitude {magnitude} in the city of {city}\n\n"
    disclaimer_msg = "Disclaimer Text : This is just a test \n\n"
    join_msg = f"To get involved join us on Slack {short_slack_invite_url}"
    twitter_msg = event_msg + disclaimer_msg + join_msg

    return twitter_msg


def coordinates_to_city(latitude, longitude):
    """Converts latitude and longitude into a city name"""
    geolocator = Nominatim(user_agent="openeew")
    coordinates_str = f"{latitude}, {longitude}"
    location = geolocator.reverse(coordinates_str)

    json_str = json.dumps(location.raw)
    json_str = json.loads(json_str)

    return json_str["address"]["city"]


run()
