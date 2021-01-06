import enum


class State(enum.Enum):
	"""Represents a Pumper state. (not pump (physical) or Pump (object) state)"""

	RUNNING = 1
	STOPPED = 2
