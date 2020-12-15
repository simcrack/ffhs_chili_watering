# concrete class represents a pump
class Pump:
	
	def __init__(self, pumpNr, gpio):
		self._pumpNr = pumpNr
		self._gpio = gpio
	
	# start pumping (activate)
	def start(self):
		# TODO: Implement
		print("Pump " + str(self._pumpNr) + " starts pumping")
	
	# stop pumping (deactivate)
	def stop(self):
		# TODO: Implement
		print("Pump " + str(self._pumpNr) + " stops pumping")
	
	def getPumpNr(self):
		return self._pumpNr