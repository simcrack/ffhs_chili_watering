import enum

class State(enum.Enum):
	"""Represents Controller states."""
	RUNNING = 1
	STOPPED = 2


class Type(enum.Enum):
	"""Represents Controller Types."""
	TEMPERATURE = 1
	HUMIDITY = 2
	LIGHT = 3
	TIME = 4
