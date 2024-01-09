from machine import Pin
import time

red = Pin(9, Pin.OUT)
green = Pin(10, Pin.OUT)
blue = Pin(11, Pin.OUT)

def cervena():
  blue.value(0)
  green.value(0)
  red.value(1)

def zelena():
  blue.value(0)
  green.value(1)
  red.value(0)

def modra():
  blue.value(1)
  green.value(0)
  red.value(0)

def fialova():
  blue.value(1)
  green.value(0)
  red.value(1)


def zhasnout():
  blue.value(0)
  green.value(0)
  red.value(0)

def shine():
  blue.value(1)
  green.value(1)
  red.value(1)

"""
while True:

    shine()
    print("shine")
    time.sleep(1)

    cervena()
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

    zhasnout()
    print("off")
    time.sleep(1)

    """