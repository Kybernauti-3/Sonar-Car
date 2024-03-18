from umqtt.simple import MQTTClient
import network
import json
import SignalLED as sl

MQTT_BROKER = "broker.emqx.io"
#MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "sonar"

def connect_mqtt():
    print("Pripojovani na MQTT")
    client = MQTTClient("pico", MQTT_BROKER)
    client.connect()
    print("Pripojeno na MQTT")
    return client
"""    try:
        print("Pripojovani na MQTT")
        client = MQTTClient("pico", MQTT_BROKER)
        client.connect()
        print("Pripojeno na MQTT")
        return client
    
    except Exception as e:
        print("An error occurred:", e)
        return None"""

def mqtt_send(data):
    payload = json.dumps(data)
    try:
        if mqtt_client is not None:  # Ověření, zda mqtt_client není None
            mqtt_client.publish(MQTT_TOPIC, payload)
        else:
            print("MQTT klient neni inicializovan. Nelze odeslat zpravu.")
    except Exception as e:
        print("Chyba pri odesilani na MQTT:", e)

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

sl.tyrkys()
connect_wifi()
sl.purple()
mqtt_client = connect_mqtt() # pripojeni na mqtt

mqtt_send("Sonar connected")