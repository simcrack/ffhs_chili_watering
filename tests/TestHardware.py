"""Provides tests for the pumper and sensor packages."""
from time import sleep

import pumper
import sensor
from pumper.Pumper import Pumper
from sensor import Type


class TestHardware(unittest.TestCase):
	"""Provides tests for the Hardware related classes."""

	def setUp(self):
		self.p = Pumper()

	def testHumSensor(self):
		"""Test reading of the humidity sensors."""
		sensors = []
		for i in range(1, 5):
			sensors[i] = sensor.createSensor(i, Type.HUMIDITY, str(i))
		for s in sensors:
			print("Hum sensor channel: " + s.channel + ", read value is" + s.getValue())

	def testTempSensor(self):
		"""Test reading of the temperature sensor."""
		temp = sensor.createSensor(
			8, Type.TEMPERATURE, "/sys/bus/w1/devices/28-3c01b556cc3d/w1_slave"
		)
		print(
			"Temperature sensor channel: "
			+ temp.channel
			+ ", read value is"
			+ temp.getValue()
		)

	def testLightSensor(self):
		"""Test reading of the light sensor."""
		light = sensor.createSensor(7, Type.LIGHT, str(7))
		print(
			"Light sensor channel: "
			+ light.channel
			+ ", read value is"
			+ light.getValue()
		)

	def testPump(self):
		"""Test the pump function of each pump"""
		pumps = pumper.Pumper()
		pumps.addPump(1, 16)
		pumps.addPump(2, 20)
		pumps.addPump(3, 21)
		pumps.addPump(4, 26)

		for p in range(1, 5):
			pumps.pump(p, 10)
			sleep(10)