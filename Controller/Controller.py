from .enums import State
import threading
import random
import time

# abstract class, represents a controller
class Controller:

	def __init__(self, pump, sensor, nr):
		self.lock = threading.Lock()
		self._pumper = pumper
		self._sensor = sensor
		self._nr = nr
		self._state = State.STOPPED
		self._stop = False

	# starts the controller
	# this function keeps running until the function
	# stop() is called from another thread
	def run(self):
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

	# not thread safe
	# getter for current state of the controller
	# does not not have to be the true state (due to non-thread-safety)
	def getState(self):
		return self._state

	# thread safe
	# stops the sensor measure loop
	def stop(self):
		self.lock.acquire(True, -1)
		try:
			self._stop = True

		finally:
			self.lock.release()
