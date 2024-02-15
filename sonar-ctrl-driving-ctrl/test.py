import machine
import time

# Nastavení pinů pro krokový motor
motor_pins = [machine.Pin(2, machine.Pin.OUT), machine.Pin(3, machine.Pin.OUT), machine.Pin(4, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT)]

# Funkce pro otočení krokového motoru o určitý počet kroků
def step_motor(steps, direction):
    step_sequence = [
        [1, 0, 0, 1],
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1]
    ]

    for _ in range(steps):
        for pin_index, pin in enumerate(motor_pins):
            pin.value(step_sequence[direction][pin_index])
        time.sleep_ms(5)  # Krátká pauza pro stabilizaci krokového motoru

# Nastavení pinů pro ultrazvukový senzor
trigger_pin = machine.Pin(21, machine.Pin.OUT)
echo_pin = machine.Pin(20, machine.Pin.IN)

# Funkce pro měření vzdálenosti pomocí ultrazvukového senzoru
def measure_distance():
    # Vyšleme krátký puls na trigger pin
    trigger_pin.value(1)
    time.sleep_us(10)
    trigger_pin.value(0)
    
    # Čekáme na změnu na echo pinu
    while echo_pin.value() == 0:
        pulse_start = time.ticks_us()
    while echo_pin.value() == 1:
        pulse_end = time.ticks_us()
    
    # Vypočteme délku pulsu a převedeme na vzdálenost v centimetrech
    pulse_duration = time.ticks_diff(pulse_end, pulse_start)
    distance_cm = pulse_duration / 58
    
    return distance_cm

# Funkce pro vytvoření mapy místnosti
def create_room_map():
    room_map = []
    
    # Počet otáček krokového motoru pro 360 stupňů
    steps_per_rotation = 512
    
    for _ in range(360):
        distances = []
        
        # Pro každý úhel se provede měření vzdálenosti
        for _ in range(5):  # Pro každý úhel provedeme 5 měření pro průměr
            distance_cm = measure_distance()
            distances.append(distance_cm)
        
        # Zpracování naměřených vzdáleností na mapu
        obstacle_detected = any(d < 20 for d in distances)  # Pokud je nějaká vzdálenost menší než 20cm, považujeme to za překážku
        room_map.append(1 if obstacle_detected else 0)
        
        # Otočení krokového motoru o jeden krok (1.8 stupně)
        step_motor(1, 0)  # 0 pro otáčení vpravo, 1 pro otáčení vlevo
        time.sleep(0.1)  # Krátká pauza pro stabilizaci
        
    return room_map

# Funkce pro uložení mapy do souboru
def save_map_to_file(room_map, filename="room_map.txt"):
    with open(filename, "w") as file:
        for value in room_map:
            file.write(str(value) + "\n")

# Hlavní smyčka
while True:
    room_map = create_room_map()
    print(room_map)  # Vytiskne vytvořenou mapu místnosti
    save_map_to_file(room_map)  # Uloží mapu do souboru
    print("Mapa uložena do souboru 'room_map.txt'")
    time.sleep(60)  # Počká 60 sekund před dalším měřením
