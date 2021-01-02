from sensor import Sensor
import settings
import configparser


class TestHumSensor(Sensor):
	def _measure(self):
		config = configparser.ConfigParser()
		config.read(settings.TESTFILE)

		return config.getfloat("Sensors", str(self.channel))
