from controller.enums import State
from pumper import Pumper
from sensor import Sensor
import controller.ruling
import threading
import time
import datetime


class Controller:
	"""Abstract class, represents a Controller.
	
	A Controller is the link between a Sensor and a Pump.
	It contains a ruleset which describes, under which sensor conditions the 
	pump should run.
	"""

	def __init__(self, pumper: Pumper, pumpNr: int, sensor: Sensor):
		"""Initialises the Controller.
		
		Args:
			pumper: A reference to an object og the Pumper class.
			pumpNr: The Pump, to which the sensor shall be bound.
			sensor: The Sensort which shall be bound to the Pump.

		Atributes:
			lock: A lock object for concurrent access on the object.
		"""
		self.lock = threading.Lock()
		self._pumper = pumper
		self._pumpNr = pumpNr
		self._sensor = sensor
		self._state = State.STOPPED
		self._stop = False

	def run(self):
		"""Starts the controller loop.

		This function keeps running until the function
		stop() is called from another thread.
		"""
		self._state = State.RUNNING
		while 1:
			# sleep ensures, that other components have also a chance to lock
			time.sleep(0.1)

			with self.lock:
				if self._stop:
					self._state = State.STOPPED
					print(str(self) + " is going down")
					break
				self._doWork()

	def _doWork(self):
		"""NOT THREAD SAFE, should be called from run() to do the work.

		This function is called periodically from the run() function.
		The run() function acquires the lock on Controller, so this must not be 
		done by doWork().
		In doWork(), you should implement the functionallity of the specific
		Controller specialisation.
		"""
		raise NotImplementedError("This Function must be overwritten in inhertied class")

	def getState(self):
		"""NOT THREAD SAFE, getter for current state of the Controller.

		Does not have to be the true state (due to non-thread-safety)
		
		Retuns:
			State.RUNNING if the Controller is running
			STATE:STOPPED else
		"""
		return self._state

	def stop(self):
		"""Thread safe, stops the controller loop"""
		with self.lock:
			self._stop = True

class MeasureRule(controller.ruling.Rule):
	def __init__(
		self,
		timeFrom: datetime.time,
		timeTo: datetime.time,
		comparator: controller.ruling.Comparator,
		rValue,
	):
		controller.ruling.Rule.__init__(self, timeFrom, timeTo)
		self.comparator = comparator
		self.rValue = rValue

	def _compare(self, currentValue):
		if self.comparator == controller.ruling.Comparator.LESSER:
			return currentValue < self.rValue
		elif self.comparator == controller.ruling.Comparator.LESSEROREQUAL:
			return currentValue <= self.rValue
		elif self.comparator == controller.ruling.Comparator.EQUAL:
			return currentValue == self.rValue
		elif self.comparator == controller.ruling.Comparator.GREATEROREQUAL:
			return currentValue >= self.rValue
		elif self.comparator == controller.ruling.Comparator.GREATER:
			return currentValue > self.rValue
		else:
			raise NotImplementedError

	def getPumpSeconds(self, currentDateTime, currentValue) -> int:
		""""""
		if self._shouldCheck(currentDateTime):
			return self._compare(currentValue)

class MeasureController(Controller):
	"""Specialised Controller for measuring sensors like HumSensor and LightSensor.
	
	A MeasureController compares Sensor values with a given constant which is
	defined inside a MeasureRule. 
	"""
	def __init__(self, pumper, pumpNr, sensor):
		"""Initialises a MeasureController.

		Is derived from the Controller class.

		Attribute:
		        ruleSet: a list of MeasureRule instances.
		        Others, see base class Controller."""
		Controller.__init__(self, pumper, pumpNr, sensor)
		self.ruleSet = []

	def addRule(self, rule: MeasureRule):
		"""Thread safe, adds an additional Rule to the Controller."""
		with self.lock:
			self.ruleSet.append(rule)

	def _doWork(self):
		"""NOT THREAD SAFE, should be called from run() to do the work.

		For details, see base Class Controller.
		"""
		for rule in self.ruleSet:
			seconds = rule.getPumpSeconds(
				datetime.datetime.now(), self._sensor.getValue()
			)
			if seconds > 0:
				self._pumper.pump(self._pumpNr, seconds)
