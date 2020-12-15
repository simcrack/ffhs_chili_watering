from . import Pump

class Pumper:
	pumps = list(Pump)

	# adds a new Pump to the Pumper
	def addPump(self, pumpNr, gpio):
		if self._getPump(pumpNr):
			raise Exception("pumpNr is already in use by another pump")			
		
		self.pumps.append(Pump(pumpNr, gpio))

	def pump(self, pumpNr, seconds):
		print("pump")

	# finds the Pump in the Pump list of Pumper, with the Nr given in argument pumpNr
	def _getPump(self, pumpNr) -> Pump:
		for pump in self.pumps:
			if pump.getPumpNr() == pumpNr:
				return pump
		return None
