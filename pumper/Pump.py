import logging

logger = logging.getLogger(__name__)

class Pump:
	"""Represents a physical Pump.
	
	"""
	def __init__(self, pumpNr, gpio):
		"""Intatiates a Pump.
		
		Attributes:
			_pumpNr : Nr (int)
			_gpio : GPIO on which the pump is attached
		"""
		self._pumpNr = pumpNr
		self._gpio = gpio
	
	def start(self):
		'''Activates the pump (start pumping).'''
		# TODO: Implement
		logger.info("Pump received start request, pumpNr: %d", self._pumpNr)
	
	def stop(self):
		'''Deactivates the pump (stop pumping).'''
		# TODO: Implement
		logger.info("Pump received stop request, pumpNr: %d", self._pumpNr)
	
	def getPumpNr(self):
		return self._pumpNr
