
from sensor.Sensor import Sensor
from sensor.enums import Type
from sensor.TempSensor import TempSensor
from sensor.HumSensor import HumSensor
from sensor.LightSensor import LightSensor

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
