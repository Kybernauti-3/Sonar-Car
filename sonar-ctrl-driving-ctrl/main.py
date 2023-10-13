import machine
import utime
import math
from machine import Pin
from utime import sleep

pin = Pin("LED", Pin.OUT)

def LED():
    print("LED")
    pin.on()
    sleep(1)
    pin.off()
    sleep(1)

LED()

# Inicializace GPIO piny pro krokový motor
motor_pins = [machine.Pin(2, machine.Pin.OUT), machine.Pin(3, machine.Pin.OUT), machine.Pin(4, machine.Pin.OUT), machine.Pin(17, machine.Pin.OUT)]
step_sequence = [[1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]]

# Inicializace GPIO piny pro HC-SR04
room_map = {}  # Mapa místnosti, kde každá buňka je 10x10 cm
robot_position = (0, 0)  # Aktuální pozice vozítka v buňkách
robot_angle_degrees = 0  # Aktuální úhel vozítka (0 stupňů je směr nahoru)

# Funkce pro získání vzdálenosti ze senzoru HC-SR04
def get_distance():
    TRIG_PIN = machine.Pin(20, machine.Pin.OUT)
    ECHO_PIN = machine.Pin(21, machine.Pin.IN)

    TRIG_PIN.value(1)
    utime.sleep_us(10)
    TRIG_PIN.value(0)
    
    while ECHO_PIN.value() == 0:
        pulse_start = utime.ticks_us()
    
    while ECHO_PIN.value() == 1:
        pulse_end = utime.ticks_us()
    
    pulse_duration = utime.ticks_diff(pulse_end, pulse_start)
    distance = pulse_duration / 58  # Vzdálenost ve cm (rychlost zvuku ve vzduchu je přibližně 343 m/s)
    
    return distance

# Funkce pro otočení krokového motoru o 90 stupňů
def rotate_motor_90_degrees():
    for i in range(512):
        for halfstep in range(8):
            for pin, value in zip(motor_pins, step_sequence[halfstep]):
                pin.value(value)
            utime.sleep_us(1000)  # Zpoždění mezi kroky

# Funkce pro aktualizaci mapy na základě dat z ultrazvukového čidla
def update_map(distance, angle_degrees):
    global room_map, robot_position, robot_angle_degrees
    
    # Převod úhlů na radiány
    angle_rad = math.radians(robot_angle_degrees + angle_degrees)
    
    # Vypočet nové pozice na mapě
    new_x = robot_position[0] + int(distance * math.cos(angle_rad) / 10)  # 10 cm za jednotku
    new_y = robot_position[1] + int(distance * math.sin(angle_rad) / 10)  # 10 cm za jednotku
    
    # Aktualizace mapy
    room_map[new_x, new_y] = 1  # Značíme buňku jako překážku
    
    # Aktualizace pozice vozítka
    robot_position = (new_x, new_y)

try:
    # Ovládání krokového motoru pro otáčení o 360 stupňů s mapováním
    for i in range(4):  # 4 zastávky o 90 stupních
        for angle_degrees in range(0, 360, 5):  # Postupné otáčení
            rotate_motor_90_degrees()
            distance = get_distance()
            update_map(distance, angle_degrees)
        
        # Po každé zastávce otočte vozítko o 90 stupňů
        rotate_motor_90_degrees()
        robot_angle_degrees += 90
    
    # Výpis výsledné mapy
    for y in range(-10, 11):
        for x in range(-10, 11):
            if (x, y) == robot_position:
                print("R", end=' ')  # Aktuální pozice vozítka
            elif (x, y) in room_map:
                print("1", end=' ')  # Překážka
            else:
                print("0", end=' ')  # Volný prostor
        print()

finally:
    # Vypnutí motoru a uvolnění GPIO pinů
    for pin in motor_pins:
        pin.value(0)