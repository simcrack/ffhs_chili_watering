"""This module contains all global settings related to the chili watering system.

It is used for the following purposes:
- Defining the configration directory.
- Defining test settings.
- Initalising the logger object.
"""

import os
import logging


# BASECONFDIR = "/var/lib/chilwater/conf/"
BASECONFDIR = os.path.join(os.getcwd(), "conf")

TESTFILE = os.path.join(BASECONFDIR, "testSetting.conf")

LOGFILE = os.path.join(os.getcwd(), "log", "chilwater.log")
LOGLEVEL = logging.INFO

logging.basicConfig(
	filename=LOGFILE,
	filemode="a",
	level=LOGLEVEL,
	format="%(asctime)s %(threadName)-12s %(levelname)-8s %(message)s",
	datefmt="%Y-%m-%d %H:%M:%S",
)

# Automaticall switch from RPi.GPIO to fake_rpigio in non-RPi environments
try:
	import RPi.GPIO
except (RuntimeError, ModuleNotFoundError):
	import fake_rpigpio.utils

	fake_rpigpio.utils.install()
	logging.getLogger(__name__).warning("Fake-RPi.GPIO was loaded")
	import RPi.GPIO
