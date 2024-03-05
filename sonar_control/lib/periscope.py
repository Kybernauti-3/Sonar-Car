# Library for stepper motor with ULN2003 driver and sonar sensor HC-SR04 on top of it
import machine
from time import sleep_us, ticks_us
import math
import SignalLED as sl

class periscope:

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
	angle_per_step = 5.625/64 # Stride angle from datasheet
	angle = 0

	def __init__(self, motor_pins, trigger_pin, echo_pin):
		"""
		Initializes a Periscope object.

		Args:
			motor_pins (list): A list of motor pins.
			trigger_pin (Pin(int)): The pin object for the trigger.
			echo_pin (Pin(int)): The pin object for the echo.

		Returns:
			None
		"""
		self.motor_pins = motor_pins
		self.trigger_pin = trigger_pin
		self.echo_pin = echo_pin

	def measure(self):
			"""
			Measures the distance using the sonar sensor.
			Returns value only after the sensor has been triggered and echo received.
			Returns:
				float: The measured distance in centimeters.
			"""
			sl.blue()
			self.trigger_pin.low()
			sleep_us(20)
			self.trigger_pin.high()
			sleep_us(10)
			self.trigger_pin.low()
			start = 0
			end = 0
			try:
				while self.echo_pin.value() == 0:
					start = ticks_us()
				while self.echo_pin.value() == 1:
					end = ticks_us()
				distance = (end - start) * 0.0343 / 2
				return distance
			except:
				print("Something went wrong while measuring distance")
				return
	
	def rotate(self, degrees):
		"""
		Rotate the periscope by the specified number of degrees.

		Args:
			degrees (float): The number of degrees to rotate the periscope.

		Returns:
			None
		"""
		sl.green()
		steps = int(degrees / self.angle_per_step)
		self.angle = (self.angle + degrees) % 360
		for _ in range(abs(steps)):
			if steps > 0:
				for halfstep in range(8):
					for pin, value in zip(self.motor_pins, self.step_sequence[halfstep]):
						pin.value(value)
					sleep_us(1000)
			else:
				for halfstep in range(8):
					for pin, value in zip(self.motor_pins, self.step_sequence[7 - halfstep]):
						pin.value(value)
					sleep_us(1000)
		self.reset_motor_pins()

	def reset_motor_pins(self):
		for pin in self.motor_pins:
			pin.value(0)

	def setAngle(self, angle):
		"""
		Sets the angle of the periscope to the nearest angle value the periscope can be set to.

		Args:
			angle (float): The angle to set the periscope to.

		Returns:
			The real angle the periscope was set to.
		"""
		self.angle = int(angle / self.angle_per_step)
		return self.angle
	
	def setStepRatio(self, ratio):
		"""
		Sets the angle per step ratio.
		Use if you have a different motor or setup, e.g. with a gearbox.

		Args:
			ratio (float): The angle per step ratio.

		Returns:
			None
		"""
		self.angle_per_step = ratio

	def getXY(self, distance):
		"""
		Returns the x and y coordinates of the periscope.

		Returns:
			tuple: The x and y coordinates of the periscope.
		"""
		x = math.cos(math.radians(self.angle)) * distance
		y = math.sin(math.radians(self.angle)) * distance
		return x, y
	
	def home(self):
		"""
		Moves the periscope to the home position.

		Returns:
			None
		"""
		self.rotate(-self.angle)
