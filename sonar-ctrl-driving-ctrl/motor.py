import machine
from utime import sleep, sleep_us, ticks_us


motor_pins = [machine.Pin(2, machine.Pin.OUT), machine.Pin(3, machine.Pin.OUT), machine.Pin(4, machine.Pin.OUT), machine.Pin(5, machine.Pin.OUT)]
step_sequence = [[1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]]
robot_angle_degrees = 0  # Aktuální úhel vozítka (0 stupňů je směr nahoru)


def rotate_motor_90_degrees():
    for i in range(512):
        for halfstep in range(8):
            for pin, value in zip(motor_pins, step_sequence[halfstep]):
                pin.value(value)
            sleep_us(1000) 

for i in range(4):  # 4 zastávky o 90 stupních
        for angle_degrees in range(0, 360, 5):  # Postupné otáčení
            rotate_motor_90_degrees()
        
        # Po každé zastávce otočte vozítko o 90 stupňů
        rotate_motor_90_degrees()
        robot_angle_degrees += 10