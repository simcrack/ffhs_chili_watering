from .Controller import Controller
from .enums import *
from .HumController import HumController
from .LightController import LightController
from .TempController import TempController
from .TimeController import TimeController


def createController(controllerType, pumper, sensor, nr):
	if controllerType == Type.HUMIDITY:
		return HumController(pumper, sensor, nr)
	elif controllerType == Type.LIGHT:
		return LightController(pumper, sensor, nr)
	elif controllerType == Type.TEMPERATURE:
		return TempController(pumper, sensor, nr)
	elif controllerType == Type.TIME:
		return TimeController(pumper, sensor, nr)
	else:
		raise NotImplementedError
