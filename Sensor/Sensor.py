from .enums import State
import threading
import time

# abstract class, represents a sensor
class Sensor:
	"""Represents a sensor.
	
	Attributes:
		lock: A Lock object which is used for thread safe altering of this object.
		channel: The channel on which the physical sensor is plugged in.
	"""
	def __init__(self, channel):
		self.lock = threading.Lock()
		self.channel = channel
		
		# current state of the sensor
		self._state = State.STOPPED
		self._stop = False
		self._value = None
	
	def run(self):
		"""Starts the sensor measure loop.

		This function keeps running until the function stop() is called from
		another thread. It measures the current sensor value regularly.
		"""
		self._state = State.RUNNING
		while 1:
			time.sleep(0.1)

			# Measuring outsyide sync block -> less blocking time
			val = self._measure() 
			
			self.lock.acquire(True, -1)
			try:
				if self._stop:
					self._state = State.STOPPED
					print(str(self) + " is going down")
					break
				self._value = val
			finally:
				self.lock.release()

	def getState(self) -> State:
		"""NOT THREAD SAFE getter for current state.
		
		Does not have to be correct (due to non-thread-safety).
		
		Returns:
			State.RUNNING, if the sensor is up and running,
			State.STOPPED else."""
		return self._state

	def getValue(self):
		"""Thread safe getter for the last measured value.
		
		Returns:
			Last measured value ofthe seonsor."""
		self.lock.acquire(True, -1)
		try:
			return self._value
		finally:
			self.lock.release()
		
	def stop(self):
		"""Thread safe, stops the sensor measure loop."""
		self.lock.acquire(True, -1)
		try:
			self._stop = True
		
		finally:
			self.lock.release()

	def _measure(self):
		"""NOT THREAD SAFE, optains and returns value from sensor.
		
		Returns:
			Measured value."""

		# Must be implemented in descendant classes for the specific sensor.
		raise NotImplementedError
