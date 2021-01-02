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
	TEST_TEMPERATURE = 11
	TEST_HUMIDITY = 12
	TEST_LIGHT = 13

	@classmethod
	def fromNumber(cls, number: int):
		"""Gets the Type-Enum for a given integer value."""
		if number == 1:
			return cls.TEMPERATURE
		elif number == 2:
			return cls.HUMIDITY
		elif number == 3:
			return cls.LIGHT
		if number == 11:
			return cls.TEST_TEMPERATURE
		elif number == 12:
			return cls.TEST_HUMIDITY
		elif number == 13:
			return cls.TEST_LIGHT
		else:
			raise NotImplementedError