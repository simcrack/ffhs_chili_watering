class Pump:
	"""Represents a physical pump."""
	def __init__(self, pumpNr, gpio):
		self._pumpNr = pumpNr
		self._gpio = gpio
	
	def start(self):
		'''Activates the pump (start pumping).'''
		# TODO: Implement
		print("Pump " + str(self._pumpNr) + " starts pumping")
	
	def stop(self):
		'''Deactivates the pump (stop pumping).'''
		# TODO: Implement
		print("Pump " + str(self._pumpNr) + " stops pumping")
	
	def getPumpNr(self):
		return self._pumpNr
