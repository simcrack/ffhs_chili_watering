"""Manages Pumps"""


from pumper.Pump import Pump
from pumper.enums import State
import threading
import time
import datetime
import logging

logger = logging.getLogger(__name__)


class _Pump(Pump):
	"""Private class for a pump extending the Pump class in Pump.py.

	It adds values and functions which are used for the pump management.
	This Class is NOT THREAD SAFE, every access to it must be secured with a
	lock (in Pumper class)"
	"""

	def __init__(self, pumpNr: int, gpio: str):
		"""See base class

		Attributes:
			seconds : Number of seconds as float for which the pump shall run.
						The pump must be stopped if it reaches 0.
			For the rest, see base class Pump
		"""
		Pump.__init__(self, pumpNr, gpio)
		self.seconds = float(0)

		# runSince is used to calculate the stop time.
		self._runSince: datetime.datetime = None

	def __del__(self):
		"""Stops the pump before the object is destroyed.

		This is a safety measurement, because the pump could run for a long time
		even if the software was stopped, if the stop command was not send.
		"""
		self.stop()

	def manageStartStop(self):
		"""Stops/starts the pump, if this has to be done.

		Recalculates the seconds based on the time ellapsed since the last call.
		"""
		if self._runSince and self.seconds <= 0:
			# Pump started, but has to be stopped
			self.stop()
			self._runSince = None

		elif not self._runSince and self.seconds > 0:
			# Pump stopped, but has to be started
			self._runSince = datetime.datetime.now()
			self.start()

		elif self._runSince:
			# Pump started, seconds have to be updated
			currentDate = datetime.datetime.now()
			self.seconds -= (currentDate - self._runSince).total_seconds()
			self._runSince = currentDate

	def immediateStop(self):
		"""Imediately stops Pump and resets control variables.

		Is used if the whole System is going down.
		"""
		self.seconds = float(0)
		self._runSince: datetime.datetime = None
		self.stop()


class _TestPump(_Pump):
	"""Private class for a test pump extending the _Pump class.

	It behaves like _Pump, but overrides the stop() and start() function
	which now simply make a log entry.
	"""

	def start(self):
		logger.info("TESTPUMP START: " + str(self._pumpNr))

	def stop(self):
		logger.info("TESTPUMP  STOP: " + str(self._pumpNr))


class Pumper:
	"""Is repsonsible for the management of all pumps.

	Runs in a separate thread and gets pump orders from other threads.
	Other threads can also create new pumps and delete exsiting ones
	with its class methods.
	"""

	def __init__(self):
		"""Inits Pumper with an empty list of pumps.
		
		Attributes:
			pump : A dict of pumps, which are managed by this pumper (pumNr is the key).
			lock : A Lock object which must be used for direct state changes of Pumper.
		"""
		self.pumps = {}
		self.lock = threading.Lock()
		self._stop: bool = None

	def run(self):
		"""Starts the pumper management loop.

		This function keeps running until the function stop() is called from
		another thread.
		It ensures that the pumps are stopped after the specified time which
		was given in the pump() function.
		"""
		logger.info("Pumper startet")
		self._state = State.RUNNING
		while 1:
			time.sleep(0.1)

			with self.lock:
				if self._stop:
					for pump in self.pumps:
						self.pumps[pump].immediateStop()

					self._state = State.STOPPED
					logger.info("Pumper is going down")
					break

				for pump in self.pumps:
					self.pumps[pump].manageStartStop()

	def stop(self):
		"""Thread safe, stops the sensor measure loop."""
		with self.lock:
			self._stop = True

	def addPump(self, pumpNr, gpio):
		"""Thread safe, instantiates a pump and adds it to the managed pump list.

		Args:
			pumpNr: Number of the pump (int).
			gpio: GPIO Pin of the pump.
		"""
		with self.lock:
			if pumpNr in self.pumps:
				raise ValueError("pumpNr is already in use by another pump")

			if gpio == 0:
				# For testing purposes for when there is no hardware available.
				self.pumps[pumpNr] = _TestPump(pumpNr, gpio)
			else:
				self.pumps[pumpNr] = _Pump(pumpNr, gpio)

	def pump(self, pumpNr: int, seconds: int) -> int:
		"""Thread safe, receives a pump order for a specific pump.

		The pump is started, on the next checking time (manageStartStop())
		and will be stopped after the time period defined in "seconds" has elapsed.
		If the pump is already running, the seconds are added to the predefined
		ones.

		Args:
			pumpNr: Number of the pump.
			seconds: For how many seconds shall the pump be activated?

		Returns:
			New value (could be equivalent to the argument "seconds", but could
			be also more than that.
		"""
		logger.info("Pump order received, pumpNr: %d, second: %d", pumpNr, seconds)
		with self.lock:

			self.pumps[pumpNr].seconds += seconds
			return self.pumps[pumpNr].seconds

	def getPumpState(self, pumpNr: int) -> str:
		"""NOT THREAD SAFE, gets a string representation of the current Pump state.

		Args:
			pumpNr: Number of the Pump.

		Returns:
			A String containing the current pump state, the datetime when the
			Pump ran lastly and the remaining number of second it has to run.
		"""
		ret = "Pumping" if self.pumps[pumpNr].isPumping() else "Stopped"
		if self.pumps[pumpNr]._runSince:
			ret += " last start: {:%Y-%m-%d %H:%M:%S}".format(
				self.pumps[pumpNr]._runSince
			)
		if self.pumps[pumpNr].seconds > 0:
			ret += " seconds remaining: {}".format(self.pumps[pumpNr].seconds)
		return ret

	def pumpExists(self, pumpNr: int) -> bool:
		"""NOT THREAD SAFE, checks, if a given pumpNr already exists.

		Args:
			pumpNr: Number of the Pump.

		Returns:
			True if the Pump already exists, else False.
		"""
		return pumpNr in self.pumps
