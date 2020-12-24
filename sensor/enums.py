import enum

# sensor states
class State(enum.Enum):
	RUNNING = 1
	STOPPED = 2

class Type(enum.Enum):
	TEMPERATURE = 1
	HUMIDITY = 2
	LIGHT = 3