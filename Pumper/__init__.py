from .Pump import Pump
from .enums import *

def createPump(pumpNr, gpio):
	return Pump(pumpNr, gpio)