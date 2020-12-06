import enum

class State(enum.Enum):
	RUNNING = 1
	STOPPED = 2

class SensorType(enum.Enum):
	TEMPERATURE = 1
	HUMIDITY = 2
	LIGHT = 3
	TIMER = 4