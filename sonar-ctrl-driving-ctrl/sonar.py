import machine
from time import sleep_us, ticks_us, sleep
import signalled as sl
from umqtt.simple import MQTTClient


# mqtt broker jen tak pro posilani nejakeho infa i tam
MQTT_BROKER = "broker.emqx.io"
#MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "sonar"

# definování pinů na kterých jsou zapojene soucastky
trigger_pin = machine.Pin(21, machine.Pin.OUT)
echo_pin = machine.Pin(20, machine.Pin.IN)
motor_pins = [machine.Pin(2, machine.Pin.OUT), machine.Pin(3, machine.Pin.OUT), machine.Pin(4, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT)]
step_sequence = [[1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]]

# velikost mapy
room_length = 10
room_width = 10

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

    mqqt_send(str(round(distance,2)))

    sleep(0.3)
    sl.off()

    return distance

# reset cívek motoru, nedela jim dobře být pod proudem jen tak
def reset_motor_pins():
    for pin in motor_pins:
        pin.value(0)

# Funkce pro otáčení motoru o 90°
def rotate_sonar():
    sl.green()
    steps_per_90_degrees = 128  # Adjust this value according to your motor and setup
    for _ in range(steps_per_90_degrees):
        for halfstep in range(8):
            for pin, value in zip(motor_pins, step_sequence[halfstep]):
                pin.value(value)
            sleep_us(1000)
    reset_motor_pins()
    sl.off()

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

# Funkce pro aktualizaci mapy na základě naměřené vzdálenosti od překážek
def update_map(distance):
    pass

# Funkce pro výpočet pozice, kam ukazuje senzor
def calculate_sensor_position(car_position):
   pass

def connect_mqtt():
    try:
        print("Pripojovani na MQTT")
        client = MQTTClient("pico", MQTT_BROKER)
        client.connect()
        print("Pripojeno na MQTT")
        return client
    
    except ConnectionError as e:
        print("Connection error occurred:", e)
        return None
    
    except Exception as e:
        print("An error occurred:", e)
        return None

def mqqt_send(data):
    try:
        if mqtt_client is not None:  # Ověření, zda mqtt_client není None
            mqtt_client.publish(MQTT_TOPIC, data)
        else:
            print("MQTT klient není inicializován. Nelze odeslat zprávu.")
    except Exception as e:
        print("Chyba při odesílání na MQTT:", e)


# Hlavní smyčka programu
try:
    mqtt_client = connect_mqtt() # pripojeni na mqtt
    room_grid = create_empty_room(room_length, room_width) # generace výchozí místnosti
    while True:
        distance = get_distance()
        
        rotate_sonar()

        measurement_count += 1
        if measurement_count % 4 == 0:
            for row in room_grid:
                print(' '.join(map(str, row)))
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
finally:
    reset_motor_pins()
    sl.off()
    print("Motor pins reset \nLED off")