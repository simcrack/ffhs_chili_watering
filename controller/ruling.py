import datetime
import controller


class Rule:
	"""Abstract class, represents a Rule for a Controller."""

	def __init__(
		self,
		name: str,
		timeFrom: datetime.time,
		timeTo: datetime.time,
		pumpSenconds: int,
	):
		"""Initialises a rule.

		A Rule is only evaluatet, if the current time corresponds to a range<>definded in the rule  (timeFrom, timeTo).
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

	def getPumpSeconds(self, currentDatetime) -> int:
		"""ABSTRACT FUNCTION. Returns the number of Second, the pump shall run.

		Checks if the rule shall be applied (only once a day) and if its
		conditions are met.
		This function must be overritten by the descendant classes.

		Args:
			currentDatetime : Present date and time.
			currentValue : Value returned by the sensor.

		Returns:
			Number of seconds if the pump shall run. If not, 0 is returned.
		"""
		raise NotImplementedError

	def _shouldCheck(self, currentDateTime):
		"""Checks if a the current timestamps meets the time span defined in the Rule."""
		return (
			self.timeFrom <= datetime.datetime.time(currentDateTime)
			and self.timeTo >= datetime.datetime.time(currentDateTime)
			and (
				# If the Rule was never used (no lastTime), it nonetheless has to
				# be a date for comparison. Thats the reason of the lambda.
				lambda a: datetime.datetime.date(a)
				if a
				else datetime.date(1970, 1, 1)
			)(self.lastRun)
			!= datetime.datetime.date(currentDateTime)
		)


class MeasureRule(Rule):
	def __init__(
		self,
		name: str,
		timeFrom: datetime.time,
		timeTo: datetime.time,
		comparator: controller.enums.Comparator,
		rValue,
		pumpSeconds,
	):
		"""Initialises a MeasureRule.

		For detail, see base class.

		Args:
			comparator : A comparator (leeser, equal, ...) used to compare sensor with rValue.
			rValue : A constant value for comparation with the current sensor value.
			For the other Arguments, see base class.
		"""
		Rule.__init__(self, name, timeFrom, timeTo, pumpSeconds)
		self.comparator = comparator
		self.rValue = rValue

	def _compare(self, currentValue):
		"""Compares the sensor value with the constant rValue."""
		if currentValue == None:
			return False
		elif self.comparator == controller.enums.Comparator.LESSER:
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

	def getPumpSeconds(self, currentDateTime: datetime.datetime, currentValue) -> int:
		"""Returns the number of Second, the pump shall run.

		For details, see base class.
		In MeasureRule, the current sensor value is compared with a given value.

		Args:
			currentValue : The current value of the sensor.
			All other arguments, see base class.
		"""
		if self._shouldCheck(currentDateTime):
			if self._compare(currentValue):
				return self.pumpSeconds
		return 0


class TimeRule(Rule):
	def getPumpSeconds(self, currentDateTime: datetime.datetime) -> int:
		"""Returns the number of Second, the pump shall run.

		For details, see base class.
		In TimeRule, there is no check if the given time intervall it becomes true.
		"""
		if self._shouldCheck(currentDateTime):
			return self.pumpSeconds
		return 0
