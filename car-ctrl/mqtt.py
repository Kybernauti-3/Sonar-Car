from umqtt.simple import MQTTClient
import network
import json

MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "sonar"
received_message = None

def connect_mqtt():
    try:
        print("Pripojovani na MQTT")
        client = MQTTClient("pico", MQTT_BROKER)
        client.connect()
        print("Pripojeno na MQTT")
        return client
   
    except Exception as e:
        print("An error occurred:", e)
        return None
    
def mqtt_callback(topic, msg):
    global received_message
    received_message = msg.decode('utf-8')

def mqtt_send(data):
    payload = json.dumps(data)
    try:
        if mqtt_client is not None:
            mqtt_client.publish(MQTT_TOPIC, payload)
        else:
            print("MQTT client is not initialized. Cannot send message.")
    except Exception as e:
        print("Error sending message to MQTT:", e)

ssid = "D31-lab"
key = "IoT.SPSE.lab22"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            pass
    print('Network config:', wlan.ifconfig())

connect_wifi()
mqtt_client = connect_mqtt() # pripojeni na mqtt

if mqtt_client is not None:
    mqtt_client.set_callback(mqtt_callback)
    mqtt_client.subscribe(MQTT_TOPIC)

mqtt_send("Buggy connected")