import machine
from comms import Communication
import mqtt

while True:
    if mqtt.mqtt_client is not None:
        mqtt.mqtt_client.wait_msg()

    if mqtt.received_message is not None:
        print(f"Message received from MQTT: {mqtt.received_message}")
        mqttmessage = mqtt.received_message.strip().lower()
        if mqttmessage == "w":
            mqtt.mqtt_send("USPECH")