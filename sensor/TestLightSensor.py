from sensor import Sensor
import settings
import configparser


class TestLightSensor(Sensor):
	"""Pseudo light sensor for testing purposes.
	
	It reads values not from a sensor but from a config file.
	For details, see class LightSensor.
	"""
	def _measure(self):
		config = configparser.ConfigParser()
		config.read(settings.TESTFILE)

		return config.getfloat("Sensors", str(self.channel))
