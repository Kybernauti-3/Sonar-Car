from machine import Pin, PWM
import time

red_pin = PWM(Pin(9), freq=5000, duty=0)  # Initialize PWM for red LED
green_pin = PWM(Pin(10), freq=5000, duty=0)  # Initialize PWM for green LED
blue_pin = PWM(Pin(11), freq=5000, duty=0)  # Initialize PWM for blue LED

def set_color(red, green, blue):
    red_pin.duty(int(red / 255 * 1023))  # Scale the 0-255 range to 0-1023 for PWM duty
    green_pin.duty(int(green / 255 * 1023))
    blue_pin.duty(int(blue / 255 * 1023))

def turn_off():
    set_color(0, 0, 0)

while True:
    # Deeper Purple color with PWM: Higher red and blue, no green
    custom_color = (255, 127, 0)  # Values in the range of 0-255
    set_color(*custom_color)
    print(f"Color: {custom_color}")
    time.sleep(2)

    turn_off()
    print("Off")
    time.sleep(1)
