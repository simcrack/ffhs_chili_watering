from controller.enums import State
import threading
import time

class Controller:
	"""Abstract class, represents a Controller.
	
	A Controller is the link between a Sensor and a Pump.
	It contains a ruleset which describes, under which sensor conditions the 
	pump should run.
	"""
	def __init__(self, pumper, pumpNr, sensor):
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
			time.sleep(0.1)
			self.lock.acquire(True, -1)
			try:
				if self._stop:
					self._state = State.STOPPED
					print(str(self) + " is going down")
					break
				# TODO: Work

			finally:
				self.lock.release()

	
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
		self.lock.acquire(True, -1)
		try:
			self._stop = True

		finally:
			self.lock.release()
