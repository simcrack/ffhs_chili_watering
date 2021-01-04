from collections.abc import Callable
import datetime
import types
from controller.enums import Comparator
import controller

class Rule:
	"""Abstract class, represents a Rule for a Controller."""

	def __init__(
		self, name:str, timeFrom: datetime.time, timeTo: datetime.time, pumpSenconds: int
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
		self.name = name

	def getPumpSeconds(self, currentDatetime, currentValue) -> int:
		raise NotImplementedError

	def _shouldCheck(self, currentDateTime):
		return (
			self.timeFrom <= datetime.datetime.time(currentDateTime)
			and self.timeTo >= datetime.datetime.time(currentDateTime)
			and datetime.datetime.date(self.lastRun) != datetime.datetime.date(currentDateTime)
		)


class MeasureRule(Rule):
	def __init__(
		self,
		name:str,
		timeFrom: datetime.time,
		timeTo: datetime.time,
		comparator: controller.enums.Comparator,
		rValue,
		pumpSeconds
	):
		Rule.__init__(self, name, timeFrom, timeTo, pumpSeconds)
		self.comparator = comparator
		self.rValue = rValue

	def _compare(self, currentValue):
		if self.comparator == controller.enums.Comparator.LESSER:
			return currentValue < self.rValue
		elif self.comparator == controller.enums.Comparator.LESSEROREQUAL:
			return currentValue <= self.rValue
		elif self.comparator == controller.enums.Comparator.EQUAL:
			return currentValue == self.rValue
		elif self.comparator == controller.enums.Comparator.GREATEROREQUAL:
			return currentValue >= self.rValue
		elif self.comparator == controller.enums.Comparator.GREATER:
			return currentValue > self.rValue
		else:
			raise NotImplementedError

	def getPumpSeconds(self, currentDateTime : datetime.datetime, currentValue) -> int:
		"""Returns the number of Second, the pump shall run.

		Checks if the rule shall be applied (only once a day) and if its 
		conditions are met.
		
		Args:
			currentDatetime : Present date and time.
			currentValie : Value returned by the sensor.
		
		Returns:
			Number of seconds if the pump shall run. If not, 0 is returned.
		"""
		if self._shouldCheck(currentDateTime):
			if self._compare(currentValue):
				return self.pumpSeconds
		return 0