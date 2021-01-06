import logging

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

logger = logging.getLogger(__name__)


class Pump:
	"""Represents a physical Pump.
	
	"""
	def __init__(self, pumpNr:int, gpio:str):
		"""Intatiates a Pump.
		
		Attributes:
			_pumpNr : Nr (int)
			_gpio : GPIO on which the pump is attached (as string).
			_pumping : True if Pump is currently pumping, else False.
		"""
		self._pumpNr = pumpNr
		self._gpio = int(gpio)
		self._pumping = False
		GPIO.setmode(GPIO.BCM)
		# Set pin gpio to be an output pin and set initial value to low(off)
		GPIO.setup(self._gpio, GPIO.OUT, initial=GPIO.HIGH)

	def start(self):
		'''Activates the pump (start pumping).'''
		GPIO.output(self._gpio, GPIO.LOW)
		self._pumping = True
		logger.info("Pump received start request, pumpNr: %d", self._pumpNr)
	
	def stop(self):
		'''Deactivates the pump (stop pumping).'''
		GPIO.output(self._gpio, GPIO.HIGH)
		self._pumping = False
		logger.info("Pump received stop request, pumpNr: %d", self._pumpNr)
	
	def getPumpNr(self):
		return self._pumpNr

	def isPumping(self):
		return self._pumping
