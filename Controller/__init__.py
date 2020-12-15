from .Controller import Controller
from .enums import *
from .HumController import HumController
from .LightController import LightController
from .TempController import TempController
from .TimeController import TimeController


def createController(controllerType : Type, pumper, pumpNr, sensor):
	if controllerType == Type.HUMIDITY:
		return HumController(pumper, pumpNr, sensor)
	elif controllerType == Type.LIGHT:
		return LightController(pumper, pumpNr, sensor)
	elif controllerType == Type.TEMPERATURE:
		return TempController(pumper, pumpNr, sensor)
	elif controllerType == Type.TIME:
		return TimeController(pumper, pumpNr, sensor)
	else:
		raise NotImplementedError
