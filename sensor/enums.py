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

	@classmethod
	def fromNumber(cls, number: int):
		"""Gets the Type-Enum for a given integer value."""
		if number == 1:
			return cls.TEMPERATURE
		elif number == 2:
			return cls.HUMIDITY
		elif number == 3:
			return cls.LIGHT
		else:
			raise NotImplementedError