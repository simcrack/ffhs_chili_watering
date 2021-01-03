from sensor import Sensor
import re, os, time

class TempSensor(Sensor):
	def _measure(self):
		value = 100
		try:
			f = open(self.channel, "r")
			line = f.readline()
			if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
				line = f.readline()
				m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
				if m:
					value = float(m.group(2)) / 1000.0
			f.close()
		except (IOError):
			print("Error reading path: ", self.channel)
		return value





