from controller.enums import State
from pumper import Pumper
from sensor import Sensor
import controller.ruling
import threading
import time
import datetime
import logging

logger = logging.getLogger(__name__)


class Controller:
	"""Abstract class, represents a Controller.

	A Controller is the link between a Sensor and a Pump.
	It contains a ruleset which describes, under which sensor conditions the
	pump should run.
	The following instances MUST be overwritten in descendants:
		_doWork()
	"""

	def __init__(self, pumper: Pumper, pumpNr: int, sensor: Sensor):
		"""Initialises the Controller.

		Args:
			pumper: A reference to an object og the Pumper class.
			pumpNr: The number of the pump which is controlled by this controller.
			sensor: The Sensor which shall be bound to the Pump.

		Atributes:
			lock: A lock object for concurrent access on the object.
			pumpNr: See Argument pumpNr.
			sensor: See Argument sensor.
		       ruleSet: a list of Rule instances.
		"""
		self.lock = threading.Lock()
		self.pumpNr = pumpNr
		self.sensor = sensor
		self.ruleSet = []
		self._pumper = pumper
		self._state = State.STOPPED
		self._stop = False

	def run(self):
		"""Starts the controller loop.

		This function keeps running until the function
		stop() is called from another thread.
		"""
		logger.info("Contoller startet for pumpNr: %d", self.pumpNr)
		logger.debug("Sensor channel: %d", self.sensor.channel)
		self._state = State.RUNNING
		while 1:
			# sleep ensures, that other components have also a chance to lock
			time.sleep(0.1)

			with self.lock:
				if self._stop:
					self._state = State.STOPPED
					logger.info("Controller is going down")
					break
				self._doWork()

	def addRule(self, rule: controller.ruling.Rule):
		"""Thread safe, adds an additional Rule to the Controller."""
		with self.lock:
			self.ruleSet.append(rule)

	def _doWork(self):
		"""NOT THREAD SAFE, Abstract function controlls the behavior of the controller.

		This function is called periodically from the run() function.
		The run() function acquires the lock on Controller, so this does not
		have to be done by _doWork().
		In _doWork(), you should implement the functionallity of the specific
		Controller specialisation.
		"""
		raise NotImplementedError(
			"This Function must be overwritten in inhertied class"
		)

	def getState(self):
		"""NOT THREAD SAFE, getter for current state of the Controller.

		Does not have to be the true state (due to non-thread-safety)

		Returns:
			State.RUNNING if the Controller is running
			STATE:STOPPED else
		"""
		return self._state

	def stop(self):
		"""Thread safe, stops the controller loop"""
		with self.lock:
			self._stop = True


class MeasureController(Controller):
	"""Specialised Controller for measuring sensors like HumSensor and LightSensor.

	A MeasureController compares a Sensor value with a given constant which is
	defined inside a MeasureRule.
	"""

	def __init__(self, pumper, pumpNr, sensor):
		"""Initialises a MeasureController.

		For functionality and attributes, see base class Controller.
		"""
		Controller.__init__(self, pumper, pumpNr, sensor)

	def _doWork(self):
		"""NOT THREAD SAFE, should be called from run() to do the work.

		For details, see base class Controller.
		"""
		currentTimeStamp = datetime.datetime.now()
		for rule in self.ruleSet:
			seconds = rule.getPumpSeconds(currentTimeStamp, self.sensor.getValue())
			if seconds > 0:
				self._pumper.pump(self.pumpNr, seconds)
				rule.lastRun = currentTimeStamp
