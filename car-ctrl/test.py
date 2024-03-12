import network
import json
from time import sleep
from machine import Pin

led = Pin("LED", Pin.OUT)
led.on()
sleep(1)
led.off()

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

led.on()
sleep(1)
led.off()
sleep(1)
led.on()
sleep(1)
led.off()