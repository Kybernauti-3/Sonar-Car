import machine
import utime

# Nastavení pinů pro první H-můstek
IN1_PIN_1 = 0
IN2_PIN_1 = 1
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

# Funkce pro pohyb doleva
def move_forward():
    IN1_1.value(0)
    IN2_1.value(1)
    IN3_1.value(1)
    IN4_1.value(0)

    IN1_2.value(1)
    IN2_2.value(0)
    IN3_2.value(0)
    IN4_2.value(1)

    utime.sleep(2)
    stop()

# Funkce pro pohyb doprava
def move_backward():
    IN1_1.value(1)
    IN2_1.value(0)
    IN3_1.value(0)
    IN4_1.value(1)

    IN1_2.value(0)
    IN2_2.value(1)
    IN3_2.value(1)
    IN4_2.value(0)

    utime.sleep(2)
    stop()

# Funkce pro pohyb doleva
def move_left():
    IN1_1.value(0)
    IN2_1.value(1)
    IN3_1.value(0)
    IN4_1.value(1)

    IN1_2.value(1)
    IN2_2.value(0)
    IN3_2.value(1)
    IN4_2.value(0)

    utime.sleep(2)
    stop()

# Funkce pro pohyb doprava
def move_right():
    IN1_1.value(1)
    IN2_1.value(0)
    IN3_1.value(1)
    IN4_1.value(0)

    IN1_2.value(0)
    IN2_2.value(1)
    IN3_2.value(0)
    IN4_2.value(1)

    utime.sleep(2)
    stop()

# Funkce pro diagonální pohyb doprava vpřed
def move_diagonal_forward_right():
    IN1_1.value(0)
    IN2_1.value(1)
    IN3_1.value(0)
    IN4_1.value(1)

    IN1_2.value(0)
    IN2_2.value(1)
    IN3_2.value(0)
    IN4_2.value(1)

    utime.sleep(2)
    stop()

# Funkce pro diagonální pohyb doprava vzad
def move_diagonal_backward_right():
    IN1_1.value(1)
    IN2_1.value(0)
    IN3_1.value(1)
    IN4_1.value(0)

    IN1_2.value(1)
    IN2_2.value(0)
    IN3_2.value(1)
    IN4_2.value(0)

    utime.sleep(2)
    stop()

# Funkce pro diagonální pohyb doleva vpřed
def move_diagonal_forward_left():
    IN1_1.value(1)
    IN2_1.value(0)
    IN3_1.value(1)
    IN4_1.value(0)

    IN1_2.value(1)
    IN2_2.value(0)
    IN3_2.value(1)
    IN4_2.value(0)

    utime.sleep(2)
    stop()

# Funkce pro diagonální pohyb doleva vzad
def move_diagonal_backward_left():
    IN1_1.value(0)
    IN2_1.value(1)
    IN3_1.value(0)
    IN4_1.value(1)

    IN1_2.value(0)
    IN2_2.value(1)
    IN3_2.value(0)
    IN4_2.value(1)

    utime.sleep(2)
    stop()


# Funkce pro zastavení
def stop():
    IN1_1.value(0)
    IN2_1.value(0)
    IN3_1.value(0)
    IN4_1.value(0)

    IN1_2.value(0)
    IN2_2.value(0)
    IN3_2.value(0)
    IN4_2.value(0)


move_forward()
utime.sleep(2)
move_backward()
utime.sleep(2)
move_left()
utime.sleep(2)
move_right()
utime.sleep(2)

while True:
    try:
        move_forward()
        utime.sleep(2)
        move_backward()
        utime.sleep(2)
        move_left()
        utime.sleep(2)
        move_right()
        utime.sleep(2)
        move_diagonal_forward_right()
        utime.sleep(2)
        move_diagonal_forward_left()
        utime.sleep(2)
        move_diagonal_backward_left()
        utime.sleep(2)
        move_diagonal_backward_right()
        utime.sleep(2)
    except KeyboardInterrupt:
        stop()