"""This module provides functions for reading and writing configuration files."""
import os
import configparser
import datetime

import pumper
import sensor
import controller


def loadControllers(
	basePath: str, pumper: pumper.Pumper, sensors: dict[sensor.Sensor]
) -> dict[controller.Controller]:
	"""Loads a Controller instance and all its Sensors from a given config directory.

	Args:
		basePath : The base dir of all conf files (/etc/chilwater/).
		pumper : Reference to a Pumper instance which holds references to all pumps.
		sensors : A lisdict of all sensors, the key represents the sensor number.

	Returns:
		A dict of all controllers, the key represents the controllerNr.
	"""
	controllers = {}
	for entry in os.scandir(os.path.join(basePath, "controllers")):
		if entry.path.endswith(".conf") and entry.is_file():
			config = configparser.ConfigParser(defaults={"SensorNr": 0})
			config.read(entry)

			if not config.has_option("DEFAULT", "Nr"):
				continue

			# The Default section in the config file describes the controller
			controllers[config.getint("DEFAULT", "Nr")] = controller.createController(
				controller.enums.Type.fromNumber(config.getint("DEFAULT", "Type")),
				pumper,
				config.getint("DEFAULT", "PumpNr"),
				# If there is no Sensor specified (TimeController), None is used.
				sensors.get(config.getint("DEFAULT", "SensorNr"), None),
			)

			if controller.enums.Type.TIME == controller.enums.Type.fromNumber(
				config.getint("DEFAULT", "Type")
			):
				getRule = _getTimeRule
			else:
				getRule = _getMeasureRule

			# Load all rules (same config file, other sections).
			for section in config.sections():
				controllers[config.getint("DEFAULT", "Nr")].addRule(
					getRule(section, section, config)
				)
	return controllers


def _getMeasureRule(ruleName: str, section: str, config: configparser.ConfigParser):
	"""Instantiates a MeasureRule with the parameters defined in config.

	Args:
		ruleName : Name of the rule.
		section : section in the config which describes the rule (usually same as ruleName)
		config : The config, loaded from a conf file.

	Returns:
		MeasureRule instance.
	"""
	return controller.MeasureRule(
		ruleName,
		datetime.datetime.strptime(config.get(section, "TimeFrom"), "%H:%M:%S").time(),
		datetime.datetime.strptime(config.get(section, "TimeTo"), "%H:%M:%S").time(),
		controller.enums.Comparator.fromString(config.get(section, "Comparator")),
		config.getfloat(section, "RightValue"),
		config.getint(section, "PumpSeconds"),
	)


def _getTimeRule(ruleName: str, section: str, config: configparser.ConfigParser):
	"""Instantiates a TimeRule with the parameters defined in config.

	Args:
		ruleName : Name of the rule.
		section : section in the config which describes the rule (usually same as ruleName)
		config : The config, loaded from a conf file.

	Returns:
		TimeRule instance.
	"""
	return controller.TimeRule(
		ruleName,
		datetime.datetime.strptime(config.get(section, "TimeFrom"), "%H:%M:%S").time(),
		datetime.datetime.strptime(config.get(section, "TimeTo"), "%H:%M:%S").time(),
		config.getint(section, "PumpSeconds"),
	)


def _getControllerFile(basePath: str, controllerNr: int) -> str:
	"""Helper function, gets the file path of a specific controller.

	Args:
		basePath : The base dir of all conf files (/etc/chilwater/).
		controllerNr : The number of the controller.

	Return:
		The full path of the configuration file if one was found, else None.
	"""
	for entry in os.scandir(os.path.join(basePath, "controllers")):
		if entry.path.endswith(".conf") and entry.is_file():
			config = configparser.ConfigParser()
			config.read(entry)

			if not config.has_option("DEFAULT", "Nr"):
				continue
			if config.getint("DEFAULT", "Nr") == controllerNr:
				return entry

	return None


def deleteController(basePath: str, controllerNr: int):
	"""Removes a Controller configuration from the config file.

	Args:
		basePath : The base dir of all conf files (/etc/chilwater/).
		controllerNr : The number of the controller which shall be removed.
	"""
	f = _getControllerFile(basePath, controllerNr)
	if not f:
		raise Exception("Conf file not found")
	os.remove(f)


def deleteRule(basePath: str, controllerNr: int, rule: str):
	"""Removes a Rule from a Controller config file.

	Args:
		basePath : The base dir of all conf files (/etc/chilwater/).
		controllerNr : The number of the controller.
		rule: The name of the rule which shall be removed.
	"""
	f = _getControllerFile(basePath, controllerNr)
	if not f:
		raise Exception("Conf file not found")

	config = configparser.ConfigParser()
	config.read(f)

	config.remove_section(rule)
	with open(f, "w") as fh:
		config.write(fh)


def editRule(basePath: str, controllerNr: int, ruleName: str, **kwargs):
	"""Adds or edits a Rule from a Controller config file.

	Args:
		basePath : The base dir of all conf files (/etc/chilwater/).
		controllerNr : The number of the controller.
		ruleName : The name of the rule which shall be altered (=section name).
			If the rule does not exists, a new rule is created.
		**kwargs : A dict with all options that shall be set.
	"""
	f = _getControllerFile(basePath, controllerNr)
	if not f:
		raise Exception("Conf file not found")

	config = configparser.ConfigParser()
	config.read(f)
	if not config.has_section(ruleName):
		config.add_section(ruleName)

	for key in kwargs:
		config.set(ruleName, key, str(kwargs[key]))

	with open(f, "w") as fh:
		config.write(fh)


def loadPumper(basePath: str) -> pumper.Pumper:
	"""Loads a Pumper instance and all its Pumps from a given config directory.

	Args:
		basePath : The base dir of all conf files (/etc/chilwater/).

	Returns:
		A Pumper objects with all Pumps defined in the config dir.
	"""
	p = pumper.Pumper()
	for entry in os.scandir(os.path.join(basePath, "pumps")):
		# Each Pump defined in pumps config dir is created and added to the Pumper.
		if entry.path.endswith(".conf") and entry.is_file():
			config = configparser.ConfigParser()
			config.read(entry)

			for section in config.sections():
				p.addPump(config.getint(section, "Nr"), config.get(section, "GPIO"))
	return p


def loadSensors(basePath: str) -> dict[sensor.Sensor]:
	"""Loads all Sensor objects defined in a given config directory.

	Args:
		basePath : The base dir of all conf files (/etc/chilwater/).

	Returns:
		A dict of Sensor objects, the key is represented by Nr.
	"""
	sensors = {}
	for entry in os.scandir(os.path.join(basePath, "sensors")):
		# Each config file is scanned (filename could be equal to sensorNr,
		# but has not to be.
		if entry.path.endswith(".conf") and entry.is_file():
			config = configparser.ConfigParser()
			config.read(entry)

			for section in config.sections():
				sensors[config.getint(section, "Nr")] = sensor.createSensor(
					config.getint(section, "Nr"),
					sensor.enums.Type.fromNumber(config.getint(section, "Type")),
					config.get(section, "Channel"),
				)
	return sensors


def getWebServerConf(basePath: str) -> dict:
	"""Loads the configuration file for the web server.

	Args:
		basePath : The base dir of all conf files (/etc/chilwater/).

	Returns:
		A dict of configuration parameters with the following structure:
		host : Hostname or IP address of the web server.
		port : Port number of the web server.
		... : Additional parameters.
		userPassword : A dict of usernames and their passwords (username as key).
	"""
	ret = {}
	config = configparser.ConfigParser()
	config.read(os.path.join(basePath, "server.conf"))

	ret["host"] = config.get("DEFAULT", "host", fallback="127.0.0.1")
	ret["port"] = config.getint("DEFAULT", "port", fallback=8080)
	ret["authEnabled"] = config.getboolean("DEFAULT", "authEnabled", fallback=False)
	ret["authRealm"] = config.get("DEFAULT", "authRealm", fallback="localhost")
	ret["baseWebDir"] = config.get(
		"DEFAULT", "baseDir", fallback=os.path.join(basePath, "..", "web")
	)

	ret["userPasswords"] = {}
	for user in config.sections():
		ret["userPasswords"][user] = config.get(user, "password")

	return ret
