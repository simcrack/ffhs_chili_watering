import datetime
import controller
import sensor


class TimeController(controller.Controller):
	"""Specialised Controller for time based sensors without measuring."""

	def __init__(self, pumper, pumpNr):
		"""Initalises a TimeController."""
		controller.Controller.__init__(self, pumper, pumpNr, sensor.EmptySensor())

	def _doWork(self):
		"""NOT THREAD SAFE, should be called from run() to do the work.

		For details, see base class Controller.
		"""
		for rule in self.ruleSet:
			seconds = rule.getPumpSeconds(datetime.datetime.now())
			if seconds > 0:
				self._pumper.pump(self.pumpNr, seconds)