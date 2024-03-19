import machine
from time import sleep

# Nastavení pinů pro první H-můstek
IN1_PIN_1 = 20
IN2_PIN_1 = 19
IN3_PIN_1 = 2
IN4_PIN_1 = 3

# Inicializace pinů pro první H-můstek
IN1_1 = machine.Pin(IN1_PIN_1, machine.Pin.OUT)
IN2_1 = machine.Pin(IN2_PIN_1, machine.Pin.OUT)
IN3_1 = machine.Pin(IN3_PIN_1, machine.Pin.OUT)
IN4_1 = machine.Pin(IN4_PIN_1, machine.Pin.OUT)

# Nastavení pinů pro druhý H-můstek
IN1_PIN_2 = 4
IN2_PIN_2 = 5
IN3_PIN_2 = 6
IN4_PIN_2 = 7

# Inicializace pinů pro druhý H-můstek
IN1_2 = machine.Pin(IN1_PIN_2, machine.Pin.OUT)
IN2_2 = machine.Pin(IN2_PIN_2, machine.Pin.OUT)
IN3_2 = machine.Pin(IN3_PIN_2, machine.Pin.OUT)
IN4_2 = machine.Pin(IN4_PIN_2, machine.Pin.OUT)


# Funkce pro zastavení <3
def stop():
    IN1_1.value(0)
    IN2_1.value(0)
    IN3_1.value(0)
    IN4_1.value(0)

    IN1_2.value(0)
    IN2_2.value(0)
    IN3_2.value(0)
    IN4_2.value(0)

# Funkce pro pohyb dopředu <3
def move_forward():
    IN1_1.value(0)
    IN2_1.value(1)
    IN3_1.value(1)
    IN4_1.value(0)

    IN1_2.value(0)
    IN2_2.value(1)
    IN3_2.value(1)
    IN4_2.value(0)

    sleep(1)
    stop()

# Funkce pro pohyb dozadu <3
def move_backward():
    IN1_1.value(1)
    IN2_1.value(0)
    IN3_1.value(0)
    IN4_1.value(1)

    IN1_2.value(1)
    IN2_2.value(0)
    IN3_2.value(0)
    IN4_2.value(1)

    sleep(1)
    stop()

# Funkce pro pohyb doprava <3
def move_right():
    IN1_1.value(0)
    IN2_1.value(1)
    IN3_1.value(0)
    IN4_1.value(1)

    IN1_2.value(1)
    IN2_2.value(0)
    IN3_2.value(1)
    IN4_2.value(0)

    sleep(1)
    stop()

# Funkce pro pohyb doleva <3
def move_left():
    IN1_1.value(1)
    IN2_1.value(0)
    IN3_1.value(1)
    IN4_1.value(0)

    IN1_2.value(0)
    IN2_2.value(1)
    IN3_2.value(0)
    IN4_2.value(1)

    sleep(1)
    stop()

# Funkce pro diagonální pohyb doleva vpřed ?
def rotate_left():
    IN1_1.value(0)
    IN2_1.value(1)
    IN3_1.value(0)
    IN4_1.value(1)

    IN1_2.value(0)
    IN2_2.value(1)
    IN3_2.value(0)
    IN4_2.value(1)

    sleep(0.3)
    stop()

# Funkce pro diagonální pohyb doprava vzad ?
def rotate_right():
    IN1_1.value(1)
    IN2_1.value(0)
    IN3_1.value(1)
    IN4_1.value(0)

    IN1_2.value(1)
    IN2_2.value(0)
    IN3_2.value(1)
    IN4_2.value(0)

    sleep(0.3)
    stop()
