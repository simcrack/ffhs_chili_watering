from sensor import Sensor
from lib.adc import MCP3008


class LightSensor(Sensor):
	"""Represents a light sensor.
	"""
	def _measure(self):
		"""Reads the Sensor

		Returns:
			Returns a normalized light value between 0 and 100.
		"""
		adc = MCP3008()
		normalized_max_value = 100
		value = adc.read(int(self.channel))
		return round((value / 1023.0 * normalized_max_value), 2)
