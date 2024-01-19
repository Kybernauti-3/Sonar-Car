import machine
import utime

# Nastavení pinů pro H-můstek
IN1_PIN = 0
IN2_PIN = 1
IN3_PIN = 2
IN4_PIN = 3
EN1_PIN = 20
EN2_PIN = 21

# Inicializace pinů
IN1 = machine.Pin(IN1_PIN, machine.Pin.OUT)
IN2 = machine.Pin(IN2_PIN, machine.Pin.OUT)
IN3 = machine.Pin(IN3_PIN, machine.Pin.OUT)
IN4 = machine.Pin(IN4_PIN, machine.Pin.OUT)
EN1 = machine.PWM(machine.Pin(EN1_PIN))
EN2 = machine.PWM(machine.Pin(EN2_PIN))

# Funkce pro pohyb vpřed
def move_forward():
    IN1.value(1)
    IN2.value(0)
    IN3.value(1)
    IN4.value(0)
    EN1.freq(1000)
    EN2.freq(1000)
    EN1.duty_u16(32768)
    EN2.duty_u16(32768)

# Funkce pro pohyb vzad
def move_backward():
    IN1.value(0)
    IN2.value(1)
    IN3.value(0)
    IN4.value(1)
    EN1.freq(1000)
    EN2.freq(1000)
    EN1.duty_u16(32768)
    EN2.duty_u16(32768)

# Funkce pro zastavení
def stop():
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)
    EN1.deinit()
    EN2.deinit()

# Ovládání motorů
while True:
    try:
        move_forward()
        utime.sleep(2)
        move_backward()
        utime.sleep(2)
        stop()
    except KeyboardInterrupt:
        stop()