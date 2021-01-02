"""Manages Pumps"""


from pumper.Pump import Pump
from pumper.enums import State
import threading
import time
import datetime

class _Pump(Pump):
	"""Private class for a pump extending the Pump class in Pump.py.
	
	It adds values and functions which are used for the pump management.
	This Class is NOT THREAD SAFE, every access to it must be secured with a
	lock (in Pumper class)"
	"""

	def __init__(self, pumpNr, gpio):
		"""See base class
		
		Attributes:
			seconds : Number of seconds as float for which the pump shall run.
						The pump must be stopped if it reaches 0.
			For the rest, see base Class "Pump"
		"""
		Pump.__init__(self, pumpNr, gpio)
		self.seconds = float(0)
		self._runSince: datetime.datetime = None

	def __del__(self):
		"""Stops the pump before the object is destroyed."""
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
			self.seconds -= datetime.datetime.microsecond(
				currentDate - self._runSince) / 1000
			self._runSince = currentDate

	def immediateStop(self):
		"""Imediately stops Pump and resets control variables.

		Is used if the whole System is going down.
		"""
		self.seconds = float(0)
		self._runSince: datetime.datetime = None
		self.stop()

class Pumper:
	"""Is repsonsible for the management of all pumps.
	
	Runs in a separate thread and gets pump orders from other threads.
	Other threads can also create new pumps and delete exsiting ones
	with its class methods.
	"""
	def __init__(self):
		"""Inits Pumper with an empty list of pumps."""
		self.pumps = {}
		self.lock = threading.Lock()
		self._stop : bool = None

	def run(self):
		"""Starts the pumper management loop.

		This function keeps running until the function stop() is called from
		another thread.
		It ensures that the pumps are stopped after the specified time which
		was given in the pump() function.
		"""
		self._state = State.RUNNING
		while 1:
			time.sleep(0.1)

			with self.lock:
				if self._stop:
					for pump in self.pumps:
						self.pumps[pump].immediateStop()

					self._state = State.STOPPED
					print(str(self) + " is going down")
					break

				for pump in self.pumps:
					self.pumps[pump].manageStartStop()

	def stop(self):
		"""Thread safe, stops the sensor measure loop."""
		with self.lock:
			self._stop = True

	def addPump(self, pumpNr, gpio):
		"""Thread safe, instantiates a pump and adds it to the managed pump 
		list.
		
		Args:
			pumpNr: Number of the pump (int).
			gpio: GPIO Pin of the pump.
		"""
		with self.lock:
			if pumpNr in self.pumps:
				raise ValueError("pumpNr is already in use by another pump")

			self.pumps[pumpNr] = _Pump(pumpNr, gpio)

	def pump(self, pumpNr, seconds) -> int:
		"""Thread safe, starts the pump and stops it after the time period 
		defined in "seconds" has elapsed.
		
		If the pump is already running, the seconds are added to the predefined
		ones.
		
		Args:
			pumpNr: Number of the pump (int).
			seconds: For how many seconds shall the pump be activated?

		Returns:
			New value (could be equivalent to the argument "seconds", but could
			be also more than that.
		"""
		with self.lock:
			if self.pumpExists(pumpNr):
				raise ValueError("pumpNr is already in use")

			self.pumps[pumpNr].seconds += seconds
			return self.pumps[pumpNr].seconds

	def pumpExists(self, pumpNr):
		"""NOT THREAD SAFE, checks, if a given pumpNr already exists.
		
		Args:
			pumpNr: Number of the pump (int).
		
		Returns:
			True if the Pump already exists, else False.
		"""
		return pumpNr in self.pumps

