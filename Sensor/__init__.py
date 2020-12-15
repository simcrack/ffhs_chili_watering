from .Sensor import Sensor
from .enums import *
from .TempSensor import TempSensor
from .HumSensor import HumSensor
from .LightSensor import LightSensor

# factory function for sensors
def createSensor(sensorType : Type, channel=0):
	if sensorType == Type.TEMPERATURE:
		return TempSensor(channel)
	elif sensorType == Type.HUMIDITY:
		return HumSensor(channel)
	elif sensorType == Type.LIGHT:
		return LightSensor(channel)
	else:
		raise NotImplementedError
