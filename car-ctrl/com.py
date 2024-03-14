from comms import Communication
from machine import Pin
from time import sleep

com1 = Communication(uart_id=0, baud_rate=9600)
com1.start()

led = Pin("LED", Pin.OUT)
led.on()
sleep(1)
led.off()

while True:
    message = ""
    message = com1.read()
    
    if message is not None:
        print(f"message received: {message.strip('\n')}")
        led.on()
        sleep(1)
        led.off()

    sleep(1)