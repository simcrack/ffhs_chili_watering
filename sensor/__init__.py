from sensor.Sensor import Sensor
from sensor.enums import Type
from sensor.TempSensor import TempSensor
from sensor.HumSensor import HumSensor
from sensor.LightSensor import LightSensor
from sensor.TestTempSensor import TestTempSensor
from sensor.TestHumSensor import TestHumSensor
from sensor.TestLightSensor import TestLightSensor

# factory function for sensors
def createSensor(sensorType: Type, channel: str = "0"):
	"""Factory function for Sensor objects.

	Args:
		sensorType: Enum (sensor.enums.Type) of Sensor type.
		channel: Channel number on which the physical sensor is attached.

	Returns:
		A Sensor instance of the given type. The Sensor is not startet yet.
	"""
	if sensorType == Type.TEMPERATURE:
		return TempSensor(channel)
	elif sensorType == Type.HUMIDITY:
		return HumSensor(channel)
	elif sensorType == Type.LIGHT:
		return LightSensor(channel)
	if sensorType == Type.TEST_TEMPERATURE:
		return TestTempSensor(channel)
	elif sensorType == Type.TEST_HUMIDITY:
		return TestHumSensor(channel)
	elif sensorType == Type.TEST_LIGHT:
		return TestLightSensor(channel)
	else:
		raise NotImplementedError
