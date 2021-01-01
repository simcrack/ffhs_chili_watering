import threading
import sensor
import controller
import pumper
import sys
import datetime
import time

if __name__ == "__main__":
	r = controller.MeasureRule(
		datetime.time(10, 0),
		datetime.time(11, 0),
		controller.ruling.Comparator.LESSEROREQUAL,
		20,
	)
	p = pumper.Pumper()
	p.addPump(1, 1)

	s = sensor.createSensor(sensor.Type.TEMPERATURE, 0)
	c = controller.createController(controller.Type.TEMPERATURE, p, 1, s)
	# x = threading.Thread(target=p.getStatus, args=(1,))
	xp = threading.Thread(target=p.run, args=())
	xs = threading.Thread(target=s.run, args=())
	xc = threading.Thread(target=c.run, args=())
	xp.start()
	xs.start()
	xc.start()
	try:
		while True:
			time.sleep(1)
			print(str(s.getState()) + " - " + str(s.getValue()))

	except KeyboardInterrupt:
		print("Main Thread is going down")

	finally:
		c.stop()
		s.stop()
		p.stop()
		xc.join()
		xp.join()
		xs.join()
