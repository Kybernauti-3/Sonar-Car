import machine
from time import sleep_us, ticks_us, sleep
import SignalLED as sl
from umqtt.simple import MQTTClient

# definování pinů na kterých jsou zapojene soucastky
trigger_pin = machine.Pin(21, machine.Pin.OUT)
echo_pin = machine.Pin(20, machine.Pin.IN)
motor_pins = [machine.Pin(2, machine.Pin.OUT), machine.Pin(3, machine.Pin.OUT), machine.Pin(4, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT)]
step_sequence = [[1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]]

# velikost mapy
room_length = 20
room_width = 20

# pomocná proměná
measurement_count = 0

# Funkce pro měření vzdálenosti pomocí ultrazvukoveho senzoru
def get_distance():

    sl.blue()

    trigger_pin.low()
    sleep_us(20)
    trigger_pin.high()
    sleep_us(10)
    trigger_pin.low()
    
    start = 0
    end = 0 
    
    while echo_pin.value() == 0:
        start = ticks_us()
    
    while echo_pin.value() == 1:
        end = ticks_us()
        
    distance = ((end - start) * 0.0343) / 2
    
    print("Vzdalenost:", round(distance, 1), "cm")

    #mqqt_send(str(round(distance,2)))

    sleep(0.3)
    sl.off()

    return distance

# reset cívek motoru, nedela jim dobře být pod proudem jen tak
def reset_motor_pins():
    for pin in motor_pins:
        pin.value(0)

smer = "F"
def rotate_sonar(smer):
    sl.green()
    steps_per_90_degrees = 128  # Adjust this value according to your motor and setup
    for _ in range(steps_per_90_degrees):
        for halfstep in range(8):
            for pin, value in zip(motor_pins, step_sequence[halfstep]):
                pin.value(value)
            sleep_us(1000)
    reset_motor_pins()
    sl.off()
    smery = ["F", "L", "B", "R"]
    index = smery.index(smer)
    novy_index = (index + 1) % len(smery)
    return smery[novy_index]


def create_empty_room(length, width):
    room_grid = [[0] * width for _ in range(length)]
    for i in range(length):
        room_grid[i][0] = 1  # First column is considered as wall
        room_grid[i][-1] = 1  # Last column is considered as wall
    for j in range(width):
        room_grid[0][j] = 1  # First row is considered as wall
        room_grid[-1][j] = 1  # Last row is considered as wall
    return room_grid

def add_obstacle(room_grid, x, y):
    if 0 < x < len(room_grid) - 1 and 0 < y < len(room_grid[0]) - 1:  # Ensure coordinates are within bounds and not blocking walls
        room_grid[x][y] = 1

def spawn_car(room_grid, x, y):
    if 0 < x < len(room_grid) - 1 and 0 < y < len(room_grid[0]) - 1:  # Ensure coordinates are within bounds and not blocking walls
        room_grid[x][y] = "S"
        return x, y
    else:
        raise ValueError("Invalid car position. Coordinates must be within the room bounds.")

def car_position():
    for i in range(len(room_grid)):
        for j in range(len(room_grid[0])):
            if room_grid[i][j] == "S":
                x, y = i, j
                return x, y  # Vrátíme nalezené souřadnice auta
    print("Car not found in the room.")
    return 5,5

def distance_to_map(distance, sonar_orientation):
    global room_grid  # Upravíme na global, abychom mohli pracovat s proměnnou room_grid

    # Získání pozice auta
    car_pos = car_position()
    x_car, y_car = car_pos
    coord = round(int(distance / 10), 0)
    print("Coord:", coord)

    if coord == 0:
        return

    if sonar_orientation == "F":
        x_sonar = x_car - coord
        y_sonar = y_car
    elif sonar_orientation == "L":
        x_sonar = x_car
        y_sonar = y_car - coord
    elif sonar_orientation == "B":
        x_sonar = x_car + coord
        y_sonar = y_car
    elif sonar_orientation == "R":
        x_sonar = x_car
        y_sonar = y_car + coord

    # Přidání překážky do mapy
    if 0 < x_sonar < len(room_grid) - 1 and 0 < y_sonar < len(room_grid[0]) - 1:
        room_grid[x_sonar][y_sonar] = 1
    else:
        print("Prekazku nelze umistit na mapu.")

def print_map(room_grid):
    print("Printing map")
    for row in room_grid:
        print(' '.join(map(str, row)))

try:
    room_grid = create_empty_room(room_length, room_width) # generace výchozí místnosti
    spawn_car(room_grid, 7, 7) # prida auto do mistnosti
    print("Initial map print")
    print_map(room_grid)
    while True:
        print()
        distance = get_distance()
        print("Smer: ", smer)
        distance_to_map(distance,smer)
        smer = rotate_sonar(smer)

        measurement_count += 1
        if measurement_count % 4 == 0:
            print_map(room_grid)
            measurement_count = 0
        
        sleep(0.7)
except KeyboardInterrupt:
    # Nastavení všech motorových pinů na hodnotu 0
    reset_motor_pins()
    sl.off()
    print("Motors reset \nLED off")
except Exception as e:
    print("Chyba:", e)
    reset_motor_pins()
    sl.off()
    print("Motor pins reset \nLED off")