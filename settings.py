"""This module contains all global Settings related to the chili watering system.

It is used for the following purposes:
- Defining the configratuon directory.
"""

import os
import logging

BASECONFDIR = "/var/lib/chilwater/conf/"
# BASECONFDIR = os.path.join(os.getcwd(), "conf")

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