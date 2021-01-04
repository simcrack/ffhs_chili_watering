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
	def index(self, controllerNr: str = "0"):
		html = ""
		with open(os.path.join(self._baseWebDir, "index.html")) as f:
			html = f.read()
		html = html.replace(
			r"<!--{{ControllerRows}}-->", self.getControllers().render()
		)
		html = html.replace(r"<!--{{Log}}-->", self.getLog().render())

		if controllerNr != "0":
			html = html.replace(
				r"<!--{{RuleRows}}-->", self.getRules(int(controllerNr)).render()
			)

		return html

	@cherrypy.expose
	def deleteRule(self, controllerNr: str = "0", ruleName: str = ""):
		"""Deletes a rule from the config file and reload the backend.

		Args:
			controllerNr : number of the controller AS STRING, whichs Rule shall be deleted.
			ruleName : Name of the rule which shall be deleted.

		Return:
			Nothing, redirects to index() with cherrypy.HTTPRedirect.
		"""
		persistanceLayer.deleteRule(settings.BASECONFDIR, int(controllerNr), ruleName)
		self._main.reload()
		raise cherrypy.HTTPRedirect("index")

	@cherrypy.expose
	def editRule(self, controllerNr: str, ruleName: str, **kwargs):
		"""

		timeFrom: str = "",
		timeTo: str = "",
		comparator: str = "",
		rightValue: float = 0,
		pumpSeconds: int = 0,
		"""
		if controllerNr == "0":
			return self.index()

		persistanceLayer.editRule(
			settings.BASECONFDIR, int(controllerNr), ruleName, **kwargs
		)

		self._main.reload()
		raise cherrypy.HTTPRedirect("index")

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
					th(""),
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
					td(
						input_(
							value="Show rules",
							onclick="window.location.href='/index?controllerNr="
							+ str(ctrl)
							+ "'",
							type="submit",
							cls="button",
							id="controller_" + str(ctrl),
						)
					),
				)
		return tbl

	def getRules(self, controllerNr: int):
		"""Gets a HTML table representation of all rules.

		Args:
			controllerNr: Number of the controller.
		"""
		tbl = div(id="rules", cls="table")
		tbl.add(
			thead(
				div(
					span("Name", cls="th len-long type-str"),
					span("From", cls="th len-mid type-time"),
					span("To", cls="th len-mid type-time"),
					span("", cls="th len-short type-str"),
					span("Right Value", cls="th len-mid time-dec"),
					span("Seconds", cls="th len-mshort time-int"),
					span("", cls="th"),
					span("", cls="th"),
					cls="tr",
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

				form(
					input_(
						type="text",
						value=rl.name,
						name="ruleName",
						cls="td len-long type-str",
					),
					input_(
						type="time",
						value=rl.timeFrom,
						name="timeFrom",
						cls="td len-mid type-time",
					),
					input_(
						type="time",
						value=rl.timeTo,
						name="timeTo",
						cls="td len-mid type-time",
					),
					select(
						option("<"),
						option("<="),
						option("="),
						option(">="),
						option(">"),
						value=rl.comparator.asString(),
						name="comparator",
						cls="td len-short type-str",
					),
					input_(
						type="number",
						value=rl.rValue,
						name="rightValue",
						cls="td len-mid type-dec",
					),
					input_(
						type="number",
						value=rl.pumpSeconds,
						name="pumpSeconds",
						min="0",
						max="3600",
						cls="td len-mshort type-int",
					),
					input_(type="hidden", name="controllerNr", value=controllerNr),
					input_(value="Save Changes", type="submit", cls="td button"),
					input_(
						value="Delete rule",
						onclick="window.location.href='/deleteRule?controllerNr="
						+ str(controllerNr)
						+ "&ruleName="
						+ rl.name
						+ "'",
						type="button",
						cls="td button",
					),
					id="rule_" + str(controllerNr) + "_" + str(rl.name),
					cls="tr",
					action="/editRule",
				)

		return tbl

	def getLog(self):
		"""Returns a HTML list representation of the latest log entries."""
		ls = ol(id="log")
		with open(settings.LOGFILE, "r") as f:
			for f in reversed(f.readlines()[-50:]):
				ls.add(li(f))
		return ls
