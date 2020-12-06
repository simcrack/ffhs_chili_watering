from .enums import State
import threading
import random
import time

# abstract class, represents a sensor
class Sensor:

	def __init__(self, gpio):
		self.lock = threading.Lock()
		self._gpio = gpio
		self._state = State.STOPPED
		self._stop = False
		self._value = None
	
	# starts the sensor
	# this function keeps running until the function
	# stop() is called from another thread 
	def run(self):
		self._state = State.RUNNING
		while 1:
			time.sleep(0.1)
			val = self._measure() #Measuring outsyide sync block -> less blocking time
			
			self.lock.acquire(True, -1)
			try:
				if self._stop:
					self._state = State.STOPPED
					print(str(self) + " is going down")
					break
				self._value = val
			finally:
				self.lock.release()

	# not thread safe
	# getter for current state of the sensor
	# does not not have to be true (due to non-thread-safety)
	def getState(self):
		return self._state

	# thread safe
	# getter for last measured value
	def getValue(self):
		self.lock.acquire(True, -1)
		try:
			return self._value
		finally:
			self.lock.release()
	
	# thread safe
	# stops the sensor measure loop
	def stop(self):
		self.lock.acquire(True, -1)
		try:
			self._stop = True
		
		finally:
			self.lock.release()

	# not thread safe
	# optains and returns value from sensor
	# must be implemented in descendant classes
	def _measure(self):
		raise NotImplementedError