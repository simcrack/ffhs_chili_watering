from Sensor.TempSensor import TempSensor
from Sensor.enums import *

def createSensor(sensorType, gpio = 0):
	if sensorType == SensorType.TEMPERATURE:
		return TempSensor(gpio)
	elif sensorType == SensorType.HUMIDITY:
		print("s")
	