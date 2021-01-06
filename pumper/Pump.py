import logging

import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library

logger = logging.getLogger(__name__)


class Pump:
	"""Represents a physical Pump."""

	def __init__(self, pumpNr: int, gpio: str):
		"""Intatiates a Pump.

		Args:
			pumpNr : Number of the Pump (identifier).
			gpio : GPIO on which the pump is attached (as string).
		"""
		self._pumpNr = pumpNr
		self._gpio = int(gpio)

		# True if Pump is currently pumping, else False.
		self._pumping = False

		GPIO.setmode(GPIO.BCM)
		# Set pin gpio to be an output pin and set initial value to high(off)
		GPIO.setup(self._gpio, GPIO.OUT, initial=GPIO.HIGH)

	def start(self):
		"""Activates the pump (start pumping)."""
		GPIO.output(self._gpio, GPIO.LOW)
		self._pumping = True
		logger.info("Pump received start request, pumpNr: %d", self._pumpNr)

	def stop(self):
		"""Deactivates the pump (stop pumping)."""
		GPIO.output(self._gpio, GPIO.HIGH)
		self._pumping = False
		logger.info("Pump received stop request, pumpNr: %d", self._pumpNr)

	def getPumpNr(self):
		"""Getter for the number of the Pump."""
		return self._pumpNr

	def isPumping(self):
		"""Getter for current pump state."""
		return self._pumping
