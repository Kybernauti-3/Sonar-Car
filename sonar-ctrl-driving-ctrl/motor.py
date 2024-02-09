import machine
from utime import sleep_us

motor_pins = [machine.Pin(2, machine.Pin.OUT), machine.Pin(3, machine.Pin.OUT), machine.Pin(4, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT)]
step_sequence = [[1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]]

def rotate_motor_90_degrees():
    steps_per_90_degrees = 128  # Adjust this value according to your motor and setup
    for _ in range(steps_per_90_degrees):
        for halfstep in range(8):
            for pin, value in zip(motor_pins, step_sequence[halfstep]):
                pin.value(value)
            sleep_us(1000)

def pause_for_1_second():
    sleep_us(1000000)

def reset_motor_pins():
    for pin in motor_pins:
        pin.value(0)

# Continuous rotation
while True:
    # Rotate the motor by 90 degrees
    rotate_motor_90_degrees()

    # Reset all motor pins to 0
    reset_motor_pins()

    # Pause for 1 second
    pause_for_1_second()
