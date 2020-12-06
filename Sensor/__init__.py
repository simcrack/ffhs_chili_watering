from .Sensor import Sensor
from .enums import *
from .TempSensor import TempSensor
from .HumSensor import HumSensor
from .LightSensor import LightSensor


def createSensor(sensorType, gpio=0):
	if sensorType == Type.TEMPERATURE:
		return TempSensor(gpio)
	elif sensorType == Type.HUMIDITY:
		return HumSensor(gpio)
	elif sensorType == Type.LIGHT:
		return LightSensor(gpio)
	else:
		raise NotImplementedError
