from machine import Pin
from utime import sleep

pin = Pin("LED", Pin.OUT)

def BLIK():
    print("LED")
    pin.on()
    sleep(1)
    pin.off()
    sleep(1)