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
					th("ControllerType"),
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
					td(c.__class__.__name__),
					td(c.sensor.nr),
					td(c.sensor.__class__.__name__),
					td(str(c.sensor.getValue() or "")),
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
				measureRule = rl.__class__.__name__ == "MeasureRule"
				if measureRule:
					self._getRuleRow(
						"edit",
						controllerNr,
						rl.name,
						rl.timeFrom,
						rl.timeTo,
						rl.pumpSeconds,
						rl.comparator,
						rl.rValue,
					)
				else:
					self._getRuleRow(
						"edit",
						controllerNr,
						rl.name,
						rl.timeFrom,
						rl.timeTo,
						rl.pumpSeconds,
					)

			self._getRuleRow(
				"new",
				controllerNr,
				"",
				"00:00:00",
				"00:00:00",
				"0",
				(lambda a: "<" if a else None)(measureRule),
				(lambda a: "0" if a else None)(measureRule),
			)
		return tbl

	def _getRuleRow(
		self,
		rowType: str,
		controllerNr,
		name,
		timeFrom,
		timeTo,
		pumpSeconds,
		comparator=None,
		rValue=None,
	):
		hiddenArg = {}
		readonlyArg = {}
		formId = ""
		if rowType == "new":
			hiddenArg["hidden"] = ""
			formId = "newRule"
		else:
			readonlyArg["readonly"] = ""
			formId = "rule_" + str(controllerNr) + "_" + str(name)
		frm = form(id=formId, cls="tr", action="/editRule",)

		frm.appendChild(
			input_(
				type="text",
				value=name,
				name="ruleName",
				cls="td len-long type-str",
				**readonlyArg,
				**hiddenArg,
			)
		)

		frm.appendChild(
			input_(
				type="time",
				value=timeFrom,
				name="timeFrom",
				cls="td len-mid type-time",
				**hiddenArg,
			)
		)

		frm.appendChild(
			input_(
				type="time",
				value=timeTo,
				name="timeTo",
				cls="td len-mid type-time",
				**hiddenArg,
			)
		)

		if comparator == None:
			# TimeRule or other non measuring.
			frm.appendChild(
				div("n/a", cls="td len-short type-str", name="comparator", **hiddenArg)
			)
			frm.appendChild(
				div("n/a", cls="td len-mid type-int", name="rightValue", **hiddenArg)
			)
		else:
			# MeasureRule
			frm.appendChild(
				select(
					option(
						"<",
						**(lambda c: dict(selected="") if c == "<" else dict())(
							comparator
						),
					),
					option(
						"<=",
						**(lambda c: dict(selected="") if c == "<=" else dict())(
							comparator
						),
					),
					option(
						"=",
						**(lambda c: dict(selected="") if c == "=" else dict())(
							comparator
						),
					),
					option(
						">=",
						**(lambda c: dict(selected="") if c == ">=" else dict())(
							comparator
						),
					),
					option(
						">",
						**(lambda c: dict(selected="") if c == ">" else dict())(
							comparator
						),
					),
					value=comparator,
					name="comparator",
					cls="td len-short type-str",
					**hiddenArg,
				)
			)

			frm.appendChild(
				input_(
					type="number",
					value=rValue,
					name="rightValue",
					cls="td len-mid type-dec",
					**hiddenArg,
				)
			)

		frm.appendChild(
			input_(
				type="number",
				value=pumpSeconds,
				name="pumpSeconds",
				min="0",
				max="3600",
				cls="td len-mshort type-int",
				**hiddenArg,
			)
		)

		frm.appendChild(
			input_(type="hidden", name="controllerNr", value=controllerNr, **hiddenArg)
		)

		frm.appendChild(
			input_(value="Save Changes", type="submit", cls="td button", **hiddenArg)
		)

		if rowType == "new":
			frm.appendChild(
				input_(
					id="buttonCreateRule",
					value="Create rule",
					onclick="addRule()",
					type="button",
					cls="td button",
				)
			)
		else:
			frm.appendChild(
				input_(
					value="Delete rule",
					onclick="window.location.href='/deleteRule?controllerNr="
					+ str(controllerNr)
					+ "&ruleName="
					+ name
					+ "'",
					type="button",
					cls="td button",
				)
			)

		return frm

	def getLog(self):
		"""Returns a HTML list representation of the latest log entries."""
		ls = ol(id="log")
		with open(settings.LOGFILE, "r") as f:
			for f in reversed(f.readlines()[-50:]):
				ls.add(li(f))
		return ls
