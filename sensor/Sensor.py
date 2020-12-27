import sensor.enums
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
		self._state = sensor.enums.State.STOPPED
		self._stop = False
		self._value = None
	
	def run(self):
		"""Starts the sensor measure loop.

		This function keeps running until the function stop() is called from
		another thread. It measures the current sensor value regularly.
		"""
		self._state = sensor.enums.State.RUNNING
		while 1:
			time.sleep(0.1)

			# Measuring outsyide sync block -> less blocking time
			val = self._measure() 
			
			with self.lock:
				if self._stop:
					self._state = sensor.enums.State.STOPPED
					print(str(self) + " is going down")
					break
				self._value = val

	def getState(self) -> sensor.enums.State:
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
		with self.lock:
			return self._value
		
	def stop(self):
		"""Thread safe, stops the sensor measure loop."""
		with self.lock:
			self._stop = True

	def _measure(self):
		"""NOT THREAD SAFE, optains and returns value from sensor.
		
		Returns:
			Measured value."""

		# Must be implemented in descendant classes for the specific sensor.
		raise NotImplementedError
