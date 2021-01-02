import threading
import sys
import datetime
import time
import os
import logging

import sensor
import pumper
import controller
import persistanceLayer
import settings

if __name__ == "__main__":
	logging.basicConfig(
		filename=settings.LOGFILE,
		filemode="w",
		level=settings.LOGLEVEL,
		format="%(asctime)s %(threadName)-12s %(levelname)-8s %(message)s",
		datefmt="%Y-%m-%d %H:%M:%S",
	)
	logging.info("Test")
	# Pumper: Load config and start the thread
	pumper = persistanceLayer.loadPumper(settings.BASECONFDIR)
	pumperThread = threading.Thread(target=pumper.run, args=(), name="pumper")
	pumperThread.start()

	# Sensors: Load config and start the threads
	sensors = persistanceLayer.loadSensors(settings.BASECONFDIR)
	sensorThreads = {}
	for sid in sensors:
		sensorThreads[sid] = threading.Thread(
			target=sensors[sid].run, args=(), name="sensor_" + str(sid)
		)
		sensorThreads[sid].start()

	# Controllers: Load config and start the threads
	controllers = persistanceLayer.loadControllers(
		settings.BASECONFDIR, pumper, sensors
	)
	controllerThreads = {}
	for cid in controllers:
		controllerThreads[cid] = threading.Thread(
			target=controllers[cid].run, args=(), name="controller_" + str(cid)
		)
		controllerThreads[cid].start()

	try:
		# while True:
		time.sleep(2)

	except KeyboardInterrupt:
		logging.info("Main Thread stopped by keyboard interrupt")

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
