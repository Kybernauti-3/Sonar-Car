from umqtt.simple import MQTTClient

MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "sonar"

def connect_mqtt():
    print("Connecting to MQTT Broker")
    client = MQTTClient("pico", MQTT_BROKER)
    client.connect()
    
    print("Connected to MQTT Broker")
    
    return client

def mqqt_send(data):
    try:
        mqtt_client.publish(MQTT_TOPIC, data)
    except Exception as e:
        print("Chyba při odesílání zprávy na MQTT server:", e)

mqtt_client = connect_mqtt()

mqqt_send("ahoj")