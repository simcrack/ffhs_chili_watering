"""
This ist the Controller Package.

Its main content is an abstract class Controller and descendants which implement this class.
A Controller links a Sensor with a pump. It describes under which Sensor conditions the pump have to be activated.
"""
from controller.Controller import Controller
from controller.enums import Type
from controller.HumController import HumController
from controller.LightController import LightController
from controller.TempController import TempController
from controller.TimeController import TimeController
from controller.ruling import MeasureRule
from controller.ruling import TimeRule
import controller.ruling


def createController(controllerType: Type, pumper, pumpNr, sensor=None):
	"""Instatiates a new Controller.

	A Controller links a Sensor with a Pump.

	Args:
		controllerType : controller.enums.Type
		pumper : Instance of the Pumper object.
		pumpNr : Number of the Pump (Pump must be added to the Pumper).
		sensor : Instance of a Sensor object (optional, i.E. not used TimeSensor).

	Returns:
		Controller object of the desired type.
	"""
	if controllerType == Type.HUMIDITY:
		return HumController(pumper, pumpNr, sensor)
	elif controllerType == Type.LIGHT:
		return LightController(pumper, pumpNr, sensor)
	elif controllerType == Type.TEMPERATURE:
		return TempController(pumper, pumpNr, sensor)
	elif controllerType == Type.TIME:
		return TimeController(pumper, pumpNr)
	else:
		raise NotImplementedError
