from sensor import Sensor
from lib.adc import MCP3008


class HumSensor(Sensor):
	"""Represents a soil moisture sensor.
	"""
	def _measure(self):
		"""Reads the Sensor

		Returns:
			Returns a normalized moisture value between 0 and 100.
		"""
		adc = MCP3008()
		normalized_max_value = 100
		offset_value = 400
		value = adc.read(int(self.channel))
		value = normalized_max_value - ((value - offset_value) / (1023.0 - offset_value) * normalized_max_value)
		return round(value, 2)
