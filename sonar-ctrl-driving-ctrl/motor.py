import machine
from utime import sleep_us, sleep

motor_pins = [machine.Pin(2, machine.Pin.OUT), machine.Pin(3, machine.Pin.OUT), machine.Pin(4, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT)]
step_sequence = [[1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]]


def reset_motor_pins():
    for pin in motor_pins:
        pin.value(0)

def rotate_motor_90_degrees():
    steps_per_90_degrees = 128  # Adjust this value according to your motor and setup
    for _ in range(steps_per_90_degrees):
        for halfstep in range(8):
            for pin, value in zip(motor_pins, step_sequence[halfstep]):
                pin.value(value)
            sleep_us(1000)
    reset_motor_pins()

try:
    # Continuous rotation
    while True:
        # Rotate the motor by 90 degrees
        rotate_motor_90_degrees()
        sleep(0.5)
except KeyboardInterrupt:
    # Nastavení všech motorových pinů na hodnotu 0
    reset_motor_pins()
    print("Motor pins reset")
