import enum

# controller states
class State(enum.Enum):
	RUNNING = 1
	STOPPED = 2


class Type(enum.Enum):
	TEMPERATURE = 1
	HUMIDITY = 2
	LIGHT = 3
	TIME = 4
