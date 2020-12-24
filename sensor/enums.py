import enum

class State(enum.Enum):
	"""Represent Sensor states."""
	RUNNING = 1
	STOPPED = 2

class Type(enum.Enum):
	"""Represent Sensor Types."""
	TEMPERATURE = 1
	HUMIDITY = 2
	LIGHT = 3
