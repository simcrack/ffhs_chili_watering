import threading
import sensor
import controller
import pumper
import sys
import datetime
import time
import persistanceLayer
import os

if __name__ == "__main__":
	baseConfigPath = os.path.join(os.getcwd(), "conf")

	# loadControllers(os.path.join(os.getcwd(), "conf"))

	# Pumper: Load config and start the thread
	pumper = persistanceLayer.loadPumper(baseConfigPath)
	pumperThread = threading.Thread(target=pumper.run, args=())
	pumperThread.start()

	# Sensors: Load config and start the threads
	sensors = persistanceLayer.loadSensors(baseConfigPath)
	sensorThreads = {}
	for sid in sensors:
		sensorThreads[sid] = threading.Thread(target=sensors[sid].run, args=())
		sensorThreads[sid].start()

	# Controllers: Load config and start the threads
	controllers = persistanceLayer.loadControllers(baseConfigPath, pumper, sensors)
	controllerThreads = {}
	for cid in controllers:
		controllerThreads[cid] = threading.Thread(target=controllers[cid].run, args=())
		controllerThreads[cid].start()

	try:
		# while True:
		time.sleep(1)

	except KeyboardInterrupt:
		print("Main Thread is going down")

	finally:
		for cid in controllers:
			controllers[cid].stop()
		for sid in sensors:
			sensors[sid].stop()
		pumper.stop()

		for cid in controllerThreads:
			controllerThreads[cid].join()
		for sid in sensorThreads:
			sensorThreads[sid].join()
		pumperThread.join()
