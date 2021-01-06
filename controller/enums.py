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

	@classmethod
	def fromNumber(cls, number: int):
		"""Gets the Type-Enum for a given integer value."""
		if number == 1:
			return cls.TEMPERATURE
		elif number == 2:
			return cls.HUMIDITY
		elif number == 3:
			return cls.LIGHT
		elif number == 4:
			return cls.TIME
		else:
			raise NotImplementedError


class Comparator(enum.Enum):
	"""Represents a mathematical expression for comparing two values.

	This Enum is used by MeasureRule/MeasureController.
	"""

	LESSER = 1
	LESSEROREQUAL = 2
	EQUAL = 3
	GREATEROREQUAL = 4
	GREATER = 5

	def asString(self) -> str:
		"""Gets the string representation of a Comparator."""
		if self == self.LESSER:
			return "<"
		elif self == self.LESSEROREQUAL:
			return "<="
		elif self == self.EQUAL:
			return "="
		elif self == self.GREATEROREQUAL:
			return ">="
		elif self == self.GREATER:
			return ">"
		else:
			raise Exception("Unknown Comparator value")

	@classmethod
	def fromString(cls, comparator: str):
		"""Converts a string into a Comparator.

		Args:
			comparator: One of the following Strings: "<", "<=", "=", ">=", ">".
		"""
		if comparator == "<":
			return cls.LESSER
		elif comparator == "<=":
			return cls.LESSEROREQUAL
		elif comparator == "=":
			return cls.EQUAL
		elif comparator == ">=":
			return cls.GREATEROREQUAL
		elif comparator == ">":
			return cls.GREATER
		else:
			raise NotImplementedError
