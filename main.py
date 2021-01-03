import signal
import threading
import sys
import datetime
import time
import os
import logging

import settings


# Automaticall switch from RPi.GPIO to fake_rpigio in non-RPi environments
try:
	import RPi.GPIO
except (RuntimeError, ModuleNotFoundError):
	import fake_rpigpio.utils

	fake_rpigpio.utils.install()
	logging.getLogger(__name__).warning("Fake-RPi.GPIO was loaded")

import sensor
import pumper
import controller
import persistanceLayer
import web.frontend


class Main:
	def __init__(self):
		self._stopRequest = False
		signal.signal(signal.SIGINT, self._shutdown)
		signal.signal(signal.SIGTERM, self._shutdown)

		self._logger = logging.getLogger(__name__)

	def _shutdown(self, signum, frame):
		self._logger.info("Signal received, signum: %d", signum)
		self._stopRequest = True

	def run(self):
		self._logger.info("#########START#########")

		# Pumper: Load config and start the thread
		self.pumper = persistanceLayer.loadPumper(settings.BASECONFDIR)
		self._pumperThread = threading.Thread(
			target=self.pumper.run, args=(), name="pumper"
		)
		self._pumperThread.start()

		# Sensors: Load config and start the threads
		self.sensors = persistanceLayer.loadSensors(settings.BASECONFDIR)
		self._sensorThreads = {}
		for sid in self.sensors:
			self._sensorThreads[sid] = threading.Thread(
				target=self.sensors[sid].run, args=(), name="sensor_" + str(sid)
			)
			self._sensorThreads[sid].start()

		# Controllers: Load config and start the threads
		self.controllers = persistanceLayer.loadControllers(
			settings.BASECONFDIR, self.pumper, self.sensors
		)
		self._controllerThreads = {}
		for cid in self.controllers:
			self._controllerThreads[cid] = threading.Thread(
				target=self.controllers[cid].run, args=(), name="controller_" + str(cid)
			)
			self._controllerThreads[cid].start()

		# Web frontend
		self._webThread = threading.Thread(
			target=web.frontend.run, args=({"main": self}), name="web_frontend"
		)
		self._webThread.start()

		try:
			while not self._stopRequest:
				time.sleep(1)
			self._logger.info("Stop request received by SIGINT/SIGTERM")

		except KeyboardInterrupt:
			self._logger.info("Stop request received by keyboard interrupt")

		finally:
			self.stop()

	def stop(self):
		for cid in self.controllers:
			self.controllers[cid].stop()
		for sid in self.sensors:
			self.sensors[sid].stop()
		self.pumper.stop()

		for cid in self._controllerThreads:
			self._controllerThreads[cid].join()
		for sid in self._sensorThreads:
			self._sensorThreads[sid].join()
		self._pumperThread.join()

		web.frontend.stop()
		self._webThread.join()

		self._logger.info("Main thread is goind down")


if __name__ == "__main__":
	main = Main()
	main.run()