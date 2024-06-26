from machine import Pin
from utime import sleep, sleep_us, ticks_us

trigger = Pin(21, Pin.OUT)
echo = Pin(20, Pin.IN)
rychlost_zvuku = 0.0343
print("ads")
def vypocet_vzdalenosti():
    trigger.low()
    sleep_us(20)
    trigger.high()
    sleep_us(10)
    trigger.low()
    
    zacatek = 0  # Define zacatek before the loops
    konec = 0  # Define konec before the loops
    
    try:
        while echo.value() == 0:
            zacatek = ticks_us()
            print("s")
        
        while echo.value() == 1:
            konec = ticks_us()
            print("d")
        
        vzdalenost = ((konec - zacatek) * rychlost_zvuku) / 2
        print("Vzdalenost je: ", vzdalenost, " cm.")
    except Exception as e:
        print("Something went wrong while measuring distance")
        print("Chyba:", e)

while True:
    vypocet_vzdalenosti()
    sleep(1)
