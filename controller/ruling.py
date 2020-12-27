from collections.abc import Callable
from datetime import datetime
import types
from controller.enums import Comparator


class Rule:
	"""Abstract class, represents a Rule for a Controller."""

	def __init__(self, timeFrom: datetime.time, timeTo: datetime.time):
		self.lastRun: datetime = None
		self.timeFrom = timeFrom
		self.timeTo = timeTo

	def getPumpSeconds(self, currentDatetime, currentValue) -> int:
		raise NotImplementedError

	def _shouldCheck(self, currentDateTime):
		return (
			self.timeFrom <= datetime.time(currentDateTime)
			and self.timeTo >= datetime.time(currentDateTime)
			and datetime.date(self.lastRun) != datetime.date(currentDateTime)
		)