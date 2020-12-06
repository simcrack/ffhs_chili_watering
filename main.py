import threading
import Sensor


s = Sensor.createSensor(Sensor.Type.TEMPERATURE)

#x = threading.Thread(target=p.getStatus, args=(1,))
x = threading.Thread(target=s.run, args=())
x.start()
try:
	while True:
		print(str(s.getState()) + " - " + str(s.getValue()))

finally:
	s.stop()
	x.join()
