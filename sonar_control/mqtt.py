from umqtt.simple import MQTTClient
import network

MQTT_BROKER = "broker.emqx.io"
#MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "sonar"

def connect_mqtt():
    try:
        print("Pripojovani na MQTT")
        client = MQTTClient("pico", MQTT_BROKER)
        client.connect()
        print("Pripojeno na MQTT")
        return client
    
    except ConnectionError as e:
        print("Connection error occurred:", e)
        return None
    
    except Exception as e:
        print("An error occurred:", e)
        return None

def mqqt_send(data):
    try:
        if mqtt_client is not None:  # Ověření, zda mqtt_client není None
            mqtt_client.publish(MQTT_TOPIC, data)
        else:
            print("MQTT klient neni inicializovan. Nelze odeslat zpravu.")
    except Exception as e:
        print("Chyba pri odesilani na MQTT:", e)

#ssid = "D31-lab"
#key = "IoT.SPSE.lab22"

ssid = "Raspberry"
key = "rpipico123"

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            pass
    print('Network config:', wlan.ifconfig())

do_connect()

mqtt_client = connect_mqtt() # pripojeni na mqtt

mqqt_send("Pico connected")