from sensor import Sensor
from sensor import MCP3008


class HumSensor(Sensor):
	def _measure(self):
		adc = MCP3008()
		normalized_max_value = 100
		offset_value = 400
		value = adc.read(int(self.channel))
		return normalized_max_value - ((value - offset_value) / (1023.0 - offset_value) * normalized_max_value)
