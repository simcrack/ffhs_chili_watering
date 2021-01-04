import cherrypy
import os
import time
import dominate
import configparser
from dominate.tags import *

import settings
import persistanceLayer


class Frontend:
	def __init__(self, main):
		conf = persistanceLayer.getWebServerConf(settings.BASECONFDIR)
		self._main = main
		self._baseWebDir = conf["baseWebDir"]
		self._userPassword = conf["userPasswords"]
		cherrypy.config.update(
			{
				"server.socket_host": conf["host"],
				"server.socket_port": conf["port"],
				"engine.autoreload.on": False,
			}
		)
		self._webConfig = {
			"/": {
				"tools.auth_basic.on": conf["authEnabled"],
				"tools.auth_basic.realm": conf["authRealm"],
				"tools.auth_basic.checkpassword": self._validatePassword,
			}
		}

	def _validatePassword(self, realm, username, password):
		return (
			username in self._userPassword and self._userPassword[username] == password
		)


	@cherrypy.expose
	def index(self, controllerNr:str="0"):
		html = ""
		with open(os.path.join(self._baseWebDir, "index.html")) as f:
			html = f.read()
		html = html.replace(
			r"<!--{{ControllerRows}}-->", self.getControllers().render()
		)
		html = html.replace(r"<!--{{Log}}-->", self.getLog().render())

		if controllerNr != "0":
			html = html.replace(r"<!--{{RuleRows}}-->", self.getRules(int(controllerNr)).render())

		return html

	@cherrypy.expose
	def deleteRule(
		self,
		controllerNr: int = "0",
		ruleName: str = ""
	):
		persistanceLayer.deleteRule(settings.BASECONFDIR, int(controllerNr), ruleName)
		self._main.reload()
		while not self._main.running and self.main._reloadRequest:
			time.sleep(0.1)
			# Wait till service restarted
		raise cherrypy.HTTPRedirect("index?controllerNr=" + controllerNr)

	@cherrypy.expose
	def editRule(
		self,
		controllerNr: int = 0,
		action: str = "list",
		rule: str = "",
		timeFrom: str = "",
		timeTo: str = "",
		comparator: str = "",
		rightValue: float = 0,
		pumpSeconds: int = 0,
	):
		if controllerNr == 0:
			return self.index()
		if action == "edit":
			pass
		elif action == "delete":
			pass

	def run(self):
		cherrypy.quickstart(self, "/", self._webConfig)

	def stop(self):
		cherrypy.engine.exit()

	def getControllers(self):
		"""Gets a HTML table representation of all loaded controllers."""
		tbl = table(id="controllers")
		tbl.add(
			thead(
				tr(
					th("Nr"),
					th("PumpNr"),
					th("PumpState"),
					th("SensorNr"),
					th("SensorType"),
					th("SensorValue"),
					th("")
				)
			)
		)
		with tbl.add(tbody()):
			for ctrl in self._main.controllers:
				c = self._main.controllers[ctrl]
				tr(
					td(ctrl),
					td(c.pumpNr),
					td(self._main.pumper.getPumpState(c.pumpNr)),
					td(c.sensor.nr),
					td(c.sensor.__class__.__name__),
					td(c.sensor.getValue()),
					td(a("Show rules", href="index?controllerNr=" + str(ctrl), cls="button")),
					id="controller_" + str(ctrl),
				)
		return tbl

	def getRules(self, controllerNr:int):
		"""Gets a HTML table representation of all rules.
		
		Args:
			controllerNr: Number of the controller.
		"""
		tbl = table(id="rules")
		tbl.add(
			thead(
				tr(
					th("Name"),
					th("Time From"),
					th("Time To"),
					th("Comparator"),
					th("Right Value"),
					th("Pump Seconds"),
					th("")
				)
			)
		)
		with tbl.add(tbody()):
			for rl in self._main.controllers[controllerNr].ruleSet:
				if rl.__class__.__name__ == "MeasureRule":
					pass
				else:
					# TODO Implement Rules for TimeSensor
					raise NotImplementedError

				tr(
					td(rl.name),
					td(str(rl.timeFrom)),
					td(str(rl.timeTo)),
					td(rl.comparator.asString()),
					td(str(rl.rValue)),
					td(str(rl.pumpSeconds)),
					td(a(
						"Delete rule",
						cls="button", 
						href="deleteRule?controllerNr=" + str(controllerNr) + "&ruleName=" + rl.name)),
					id="rule_" + str(controllerNr) + "_" + str(rl.name),
				)
		return tbl
	
	def getLog(self):
		"""Returns a HTML list representation of the latest log entries."""
		ls = ol(id="log")
		with open(settings.LOGFILE, "r") as f:
			for f in reversed(f.readlines()[-50:]):
				ls.add(li(f))
		return ls