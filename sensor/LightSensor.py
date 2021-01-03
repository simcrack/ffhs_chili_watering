from sensor import Sensor
from sensor import MCP3008


class LightSensor(Sensor):
	def _measure(self):
		adc = MCP3008()
		normalized_max_value = 100
		value = adc.read(int(self.channel))
		return value / 1023.0 * normalized_max_value
