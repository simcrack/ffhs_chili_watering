from sensor import Sensor
from lib.adc import MCP3008


class EmptySensor(Sensor):
	"""Dummy sensor class, used by TimeController."""

	def __init__(self):
		"""Iitialises the EmptySensor with dummy values."""
		Sensor.__init__(self, 0, 0)

	def _measure(self):
		"""Reads the Sensor, but since there is none, returns always None."""
		return None
