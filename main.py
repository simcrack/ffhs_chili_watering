"""This is the main script of the chili watering system."""
import signal
import threading
import sys
import datetime
import time
import os
import logging

import settings

import sensor
import pumper
import controller
import persistanceLayer
import web.frontend


class Main:
	"""Controller class for main thread."""

	def __init__(self):
		"""Initialises the main thread."""
		self._stopRequest = False
		self._reloadRequest = True
		self._logger = logging.getLogger(__name__)
		signal.signal(signal.SIGINT, self._shutdown)
		signal.signal(signal.SIGTERM, self._shutdown)

	def _shutdown(self, signum, frame):
		"""Send a stop command to the main thrad.

		Args are provided from the system (signal parameters).
		"""
		self._logger.info("Signal received, signum: %d", signum)
		self._stopRequest = True

	def reload(self):
		"""Reloads config and restart all threads.

		This function will remain active until the services have restarted.
		"""
		self._stopRequest = True
		self._reloadRequest = True

		while not self._running and self._reloadRequest:
			time.sleep(0.1)

	def run(self):
		"""Starts the main loop and its child threads."""
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

		# Main loop.
		try:
			self._running = True
			while not self._stopRequest:
				time.sleep(1)
			self._logger.info("Stop request received by SIGINT/SIGTERM")
			self._running = False

		except KeyboardInterrupt:
			self._logger.info("Stop request received by keyboard interrupt")

		finally:
			self.stop()

	def stop(self):
		"""Sends a stop command to all child threads and joins them back to the main thread."""
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

		self._logger.info("Main thread is goind down")


if __name__ == "__main__":
	main = Main()

	# Web frontend
	web = web.frontend.Frontend(main)
	webThread = threading.Thread(target=web.run, args=(), name="web_frontend")
	webThread.start()

	# The backend can be reloaded by the web frontend
	# this loop keeps running also if the main thread and its child threads are restarted.
	while main._reloadRequest:
		main._reloadRequest = False
		main._stopRequest = False
		main.run()

	web.stop()
	webThread.join()
