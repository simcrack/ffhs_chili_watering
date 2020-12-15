import threading
import Sensor
import Controller

s = Sensor.createSensor(Sensor.Type.TEMPERATURE)
c = Controller.createController(Controller.Type.TEMPERATURE, 'pumper', 1, s)
#x = threading.Thread(target=p.getStatus, args=(1,))
xs = threading.Thread(target=s.run, args=())
xc = threading.Thread(target=c.run, args=())
xs.start()
xc.start()
try:
	while True:
		print(str(s.getState()) + " - " + str(s.getValue()))
		
except KeyboardInterrupt:
	print("Main Thread is going down")
	
finally:
	s.stop()
	c.stop()
	xs.join()
	xc.join()
