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

class Comparator(enum.Enum):
	LESSER = 1
	LESSEROREQUAL = 2
	EQUAL = 3
	GREATEROREQUAL = 4
	GREATER = 5