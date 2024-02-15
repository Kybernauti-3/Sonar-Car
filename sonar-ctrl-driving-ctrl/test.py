import machine
from utime import sleep_us, ticks_us

# Pinout pro krokový motor
motor_pins = [machine.Pin(2, machine.Pin.OUT), machine.Pin(3, machine.Pin.OUT), machine.Pin(4, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT)]

# Pinout pro ultrazvukový senzor
trigger = machine.Pin(21, machine.Pin.OUT)
echo = machine.Pin(20, machine.Pin.IN)

# Sekvence kroků pro krokový motor (poloviční kroky)
step_sequence = [[1, 0, 0, 1],
                 [1, 0, 0, 0],
                 [1, 1, 0, 0],
                 [0, 1, 0, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 1],
                 [0, 0, 0, 1]]

def rotate_motor_90_degrees():
    steps_per_90_degrees = 128  # Adjust this value according to your motor and setup
    for _ in range(steps_per_90_degrees):
        for halfstep in range(8):
            for pin, value in zip(motor_pins, step_sequence[halfstep]):
                pin.value(value)
            sleep_us(1000)

def measure_distance():
    trigger.value(0)
    sleep_us(2)
    trigger.value(1)
    sleep_us(10)
    trigger.value(0)

    while echo.value() == 0:
        pulse_start = ticks_us()
    while echo.value() == 1:
        pulse_end = ticks_us()

    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 0.0343) / 2  # Vzdálenost v centimetrech
    return distance

def create_room_map():
    room_map = []
    for _ in range(36):  # Předpokládáme mapu 6x6 (pro jednoduchost)
        room_map.append([0] * 36)

    for i in range(36):
        rotate_motor_90_degrees()  # Otočení o 90 stupňů
        for j in range(36):
            distance = measure_distance()
            if distance < 10:  # Pokud je překážka blíže než 10 cm
                room_map[i][j] = 1
            else:
                room_map[i][j] = 0
    return room_map

def print_map(room_map):
    for row in room_map:
        print(''.join(str(cell) for cell in row))

def main():
    room_map = create_room_map()
    print_map(room_map)

if __name__ == "__main__":
    main()
