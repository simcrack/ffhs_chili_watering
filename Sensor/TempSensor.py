#!/usr/bin/python
from Sensor.Sensor import Sensor

class TempSensor(Sensor):
	_inputQueue = 0

	def setInputQueue(inputQueue):
		self._inputQueue = inputQueue