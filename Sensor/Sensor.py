from Sensor.enums import *
import threading
import random
import time

class Sensor:

	def __init__(self, gpio):
		self.lock = threading.Lock()
		self._gpio = gpio
		self._state = State.STOPPED
		self._stop = False
		self._value = None
	
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

	#not thread safe
	def getState(self):
		return self._state

	#thread safe
	#getter
	def getValue(self):
		self.lock.acquire(True, -1)
		try:
			return self._value
		finally:
			self.lock.release()
	
	#thread safe
	#setter to send a stop command
	def stop(self):
		self.lock.acquire(True, -1)
		try:
			self._stop = True
		
		finally:
			self.lock.release()

	#not thread safe
	#must be called synchronized
	#optains and returns value from sensor
	def _measure(self):
		return random.randint(1, 100)