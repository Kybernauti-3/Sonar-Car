from machine import Pin
from comms import Communication
from time import sleep
from rotate import *
import mqtt

com1 = Communication(uart_id=0, baud_rate=9600)


while True:
    mqtt.received_message = None

    mqtt.mqtt_client.check_msg()

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
        elif mqttmessage == "q":
            rotate_left()
        elif mqttmessage == "e":
            rotate_right()
        else:
            print("Nothing mqtt")

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
            print("Nothing uart")
    sleep(1)