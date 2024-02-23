import machine
from time import sleep_us, ticks_us, sleep
import signalled as sl
from umqtt.simple import MQTTClient

MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "sonar"

# Definice pinů
trigger_pin = machine.Pin(21, machine.Pin.OUT)
echo_pin = machine.Pin(20, machine.Pin.IN)
motor_pins = [machine.Pin(2, machine.Pin.OUT), machine.Pin(3, machine.Pin.OUT), machine.Pin(4, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT)]
step_sequence = [[1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]]

# Konfigurace mapy místnosti
map_width = 7  # Šířka mapy (počet sloupců)
map_height = 7  # Výška mapy (počet řádků)
room_map = [[0] * map_width for _ in range(map_height)]  # Inicializace prázdné mapy

# Proměnná pro sledování počtu provedených měření
measurement_count = 0

# Funkce pro měření vzdálenosti pomocí sonaru
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
    
    print("Vzdalenost:", round(distance, 1), " cm")

    mqqt_send(str(round(distance,2)))


    sleep(0.5)
    sl.off()

    return distance

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

# Funkce pro aktualizaci mapy na základě naměřené vzdálenosti od překážek
def update_map(distance):
    car_position = (map_width // 2, map_height // 2)
    
    # Určení maximální vzdálenosti, která ještě bude považována za volné místo
    max_distance = 400 
    
    # Získání pozice, kam ukazuje senzor
    sensor_position = calculate_sensor_position(car_position)
    
    # Aktualizace mapy na pozici, kam ukazuje senzor
    room_map[sensor_position[0]][sensor_position[1]] = "S"  # Označení místa senzorem
    
    # Pro ostatní pozice na mapě označíme překážky nebo volné místo podle vzdálenosti
    for i in range(map_height):
        for j in range(map_width):
            if (i, j) != sensor_position:
                if abs(sensor_position[0] - i) <= 1 and abs(sensor_position[1] - j) <= 1:
                    # Pokud je pozice v okolí senzoru, zkontrolujeme vzdálenost
                    if distance < max_distance:
                        room_map[i][j] = 1  # Označení jako překážku
                    else:
                        room_map[i][j] = 0  # Označení jako volné místo
                else:
                    # Pokud je pozice daleko od senzoru, označíme ji jako volné místo
                    room_map[i][j] = 0


# Funkce pro výpočet pozice, kam ukazuje senzor
def calculate_sensor_position(car_position):
    # Tuto funkci upravte podle vašeho konkrétního zapojení a rozmístění senzoru
    sensor_position = (4, 4)  # Příklad: Senzor je pevně umístěn přímo vpředu
    
    return sensor_position

def connect_mqtt():
    client = MQTTClient("pico", MQTT_BROKER)
    client.connect()
    
    print("Connected to MQTT Broker")
    
    return client

mqtt_client = connect_mqtt()

def mqqt_send(data):
    try:
        mqtt_client.publish(MQTT_TOPIC, data)
    except Exception as e:
        print("Chyba při odesílání zprávy na MQTT server:", e)


# Hlavní smyčka programu
try:
    while True:
        distance = get_distance()
        update_map(distance)
        rotate_sonar()

        measurement_count += 1
        if measurement_count % 4 == 0:
            #print("Map:")
            for row in room_map:
                print(row)
        
        sleep_us(500000)
except KeyboardInterrupt:
    # Nastavení všech motorových pinů na hodnotu 0
    reset_motor_pins()
    sl.off()
    print("Motors reset \nLED reset")