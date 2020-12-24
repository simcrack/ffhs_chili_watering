from controller.Controller import Controller
from controller.enums import Type
from controller.HumController import HumController
from controller.LightController import LightController
from controller.TempController import TempController
from controller.TimeController import TimeController

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
