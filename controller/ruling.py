from collections.abc import Callable
from datetime import datetime
import types
from controller.enums import Comparator


class Rule:
	"""Abstract class, represents a Rule for a Controller."""

	def __init__(
		self, timeFrom: datetime.time, timeTo: datetime.time, pumpSenconds: int
	):
		"""Initialises a rule
		
		A Rule is only evaluatet, if the current time corresponds to a range 
		definded in the rule  (timeFrom, timeTo).
		Also, the Rule is applied only once a day. To ensure that, it holds
		the timestamp of the last run in an instance variable (lastRun).
		
		Attributes:
			lastRun : Last time, the Rule was checked.
			timeFrom : Lowerbound of the Rule validity timespan.
			timeTo : Upperbound of the Rule validity timespan.
			pumpSeconds : Number of seconds for which the pump shall run if the Rule is applied.
		"""
		self.lastRun: datetime = None
		self.timeFrom = timeFrom
		self.timeTo = timeTo
		self.pumpSeconds = pumpSenconds

	def getPumpSeconds(self, currentDatetime, currentValue) -> int:
		raise NotImplementedError

	def _shouldCheck(self, currentDateTime):
		return (
			self.timeFrom <= datetime.time(currentDateTime)
			and self.timeTo >= datetime.time(currentDateTime)
			and datetime.date(self.lastRun) != datetime.date(currentDateTime)
		)