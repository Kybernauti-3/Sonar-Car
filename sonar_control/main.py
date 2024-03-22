# Main program for the sonar control system
# Draws 32 by 32 grid with walls and empty space
# grid points will be 10 cm apart
# Point value will represent probability of wall, 0 - no wall, 100 - wall

# Import necessary libraries
import periscope
import SignalLED as sl
from machine import Pin
import machine
from time import sleep
import mqtt
import where2go
from comms import Communication
import gc
gc.enable()

com1 = Communication(uart_id=0, baud_rate=9600)

# Define pins for the motor and sonar
motor_pins = [Pin(2, Pin.OUT), Pin(3, Pin.OUT), Pin(4, Pin.OUT), Pin(5, Pin.OUT)]
trigger_pin = Pin(21, Pin.OUT)
echo_pin = Pin(20, Pin.IN)

grid_size = 32		# Size of the grid (in points)
point_distance = 10	# Distance between points in cm

# Create a periscope object
scope = periscope.periscope(motor_pins, trigger_pin, echo_pin)

#map_plane = [[0 for i in range(grid_size)] for j in range(grid_size)]

def spawn_car(map_plane, x, y):
    if 0 < x < len(map_plane) - 1 and 0 < y < len(map_plane[0]) - 1:  # Ensure coordinates are within bounds and not blocking walls
        map_plane[x][y] = "S"
        return x, y
    else:
        raise ValueError("Invalid car position. Coordinates must be within the room bounds.")

angle_per_step = 21.97265625 # With the gearbox

def main():
	try:
		scope.setAngle(0)
		scope.setStepRatio(angle_per_step)
		print("Map is set to " + str(grid_size) + "x" + str(grid_size) + " grid with " + str(point_distance) + " cm distance between points (" + str(grid_size*point_distance) + "x" + str(grid_size*point_distance) + " cm) \nPlease wait for map to create...")
		mqtt.mqtt_send("Map is set to " + str(grid_size) + "x" + str(grid_size) + " grid with " + str(point_distance) + " cm distance between points (" + str(grid_size*point_distance) + "x" + str(grid_size*point_distance) + " cm). Please wait for map to create...")
		while True:
			map_plane = [[0 for i in range(grid_size)] for j in range(grid_size)]

			for i in range(0, 360, 5):
				print("Rotating...")
				scope.rotate(i)
				sleep(0.1)
				print("Measuring...")
				distance = scope.measure()
				print("Angle: ", str(i), " Distance: ", str(distance))
				x,y = scope.getXY(distance)
				print("XY1 ok")
				x, y = int(x/point_distance), int(y/point_distance)
				print("XY2 ok")
				if x < grid_size and y < grid_size:
					try:
						map_plane[int(grid_size/2 + x)][int(grid_size/2 + y)] += 1
					except:
						print("Out of range, may be a sensor failure")

			gc.collect()
			print("Scan finished. Printing map:")
			sl.red()
			spawn_car(map_plane, int(grid_size/2), int(grid_size/2))
			"""for i in range(grid_size):
				print(str(map_plane[i]))"""
			mqtt.mqtt_send(map_plane)

			pohyb = where2go.GenerateMove(map_plane)
			com1.send(pohyb)

			mqtt.mqtt_send("Program Done...")
			print("Program Done...")
			sleep(1)

	except OSError:
		machine.reset()
	except Exception as e:
		print("An unexpected error occurred:", e)
		mqtt.mqtt_send(f"An unexpected error occurred: {e}")
		sl.off()

if __name__ == "__main__":
	print("Sleeping 3s")
	gc.collect()
	sleep(3)
	main()
