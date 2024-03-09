import machine
from comms import Communication
from time import sleep
from rotate import *
import mqtt

com1 = Communication(uart_id=0, baud_rate=9600)
com1.start()

while True:
    if mqtt.mqtt_client is not None:
        mqtt.mqtt_client.wait_msg()

    if mqtt.received_message is not None:
        print(f"Message received from MQTT: {mqtt.received_message}")
        mqttmessage = mqtt.received_message.strip().lower()
        if mqttmessage == "w":
            move_forward()
        elif mqttmessage == "s":
            move_backward()
        elif mqttmessage == "a":
            move_left()
        elif mqttmessage == "d":
            move_right()
        else:
            print("Error")
        mqtt.received_message = None

    message = ""
    message = com1.read()
    
    if message is not None:
        print(f"Message received: {message.strip('\n')}")

        if message == "Move up":
            move_forward()
        elif message == "Move down":
            move_backward()
        elif message == "Move left":
            move_left()
        elif message == "Move right":
            move_right()
        else:
            print("Error")

    sleep(1)