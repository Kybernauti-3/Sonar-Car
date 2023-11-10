import machine
from utime import sleep, sleep_us, ticks_us
import math
import json
import led

led.BLIK()  # Proč ne, že? ;)

# Inicializace GPIO piny pro krokový motor
motor_pins = [machine.Pin(2, machine.Pin.OUT), machine.Pin(3, machine.Pin.OUT), machine.Pin(4, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT)]
step_sequence = [[1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]]

# Inicializace mapy a pozice vozítka
room_map = {}  # Mapa místnosti, kde každá buňka je 10x10 cm
robot_position = (0, 0)  # Aktuální pozice vozítka v buňkách
robot_angle_degrees = 0  # Aktuální úhel vozítka (0 stupňů je směr nahoru)

# Funkce pro získání vzdálenosti ze senzoru HC-SR04
def get_distance():
    trigger = machine.Pin(21, machine.Pin.OUT)
    echo = machine.Pin(20, machine.Pin.IN)
    rychlost_zvuku = 0.0343

    trigger.low()
    sleep_us(20)
    trigger.high()
    sleep_us(10)
    trigger.low()
    
    zacatek = 0  # Define zacatek before the loops
    konec = 0  # Define konec before the loops
    
    while echo.value() == 0:
        zacatek = ticks_us()
    
    while echo.value() == 1:
        konec = ticks_us()
    distance = ((konec - zacatek) * rychlost_zvuku) / 2
    
    print("Vzdalenost:", distance)  # Přidáno logování
    return distance

# Funkce pro otočení krokového motoru o 90 stupňů
def rotate_motor_90_degrees():
    for i in range(512):
        for halfstep in range(8):
            for pin, value in zip(motor_pins, step_sequence[halfstep]):
                pin.value(value)
            sleep_us(1000)  # Zpoždění mezi kroky

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

    # Výpis výsledné mapy
    print_map()

# Funkce pro výpis celé mapy
def print_map():
    for y in range(-10, 11):
        for x in range(-10, 11):
            if (x, y) == robot_position:
                print("R", end=' ')  # Aktuální pozice vozítka
            elif (x, y) in room_map:
                print("1", end=' ')  # Překážka
            else:
                print("0", end=' ')  # Volný prostor
        print()
# Funkce pro uložení mapy do souboru
def save_map(filename):
    with open(filename, 'w') as file:
        json.dump(room_map, file)

    print("Mapa ulozena do souboru:", filename)  # Přidáno logování

# Funkce pro načtení nové pozice vozítka ze sdíleného souboru
def get_new_robot_position(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data["position"]
    except OSError:
        return None

# Sdílený soubor pro komunikaci s řídícím skriptem
shared_filename = "shared_data.json"

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

    # Uložení mapy po každém mapovacím cyklu
    save_map("room_map.json")

    # Zde můžete periodicky číst novou pozici vozítka ze sdíleného souboru
    while True:
        new_position = get_new_robot_position(shared_filename)
        if new_position:
            robot_position = new_position

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