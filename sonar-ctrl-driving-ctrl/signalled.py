from machine import Pin
import time

redled = Pin(9, Pin.OUT)
greenled = Pin(10, Pin.OUT)
blueled = Pin(11, Pin.OUT)

def red():
  blueled.value(0)
  greenled.value(0)
  redled.value(1)

def green():
  blueled.value(0)
  greenled.value(1)
  redled.value(0)

def blue():
  blueled.value(1)
  greenled.value(0)
  redled.value(0)

def purple():
  blueled.value(1)
  greenled.value(0)
  redled.value(1)

def tyrkys():
  blueled.value(1)
  greenled.value(1)
  redled.value(0)

def redgreen():
  blueled.value(0)
  greenled.value(1)
  redled.value(1)

def off():
  blueled.value(0)
  greenled.value(0)
  redled.value(0)

def shine():
  blueled.value(1)
  greenled.value(1)
  redled.value(1)

"""
while True:

    shine()
    print("shine")
    time.sleep(1)

    red()
    print("1")
    time.sleep(1)

    zelena()
    print("2")
    time.sleep(1)

    modra()
    print("3")
    time.sleep(1)

    fialova()
    print("4")
    time.sleep(1)

    tyrkys()
    print("5")
    time.sleep(1)

    redledgreenled()
    print("6")
    time.sleep(1)

    zhasnout()
    print("off")
    time.sleep(1)
"""