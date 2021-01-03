"""This module contains all global Settings related to the chili watering system.

It is used for the following purposes:
- Defining the configratuon directory.
"""

import os
import logging

BASECONFDIR = os.path.join(os.getcwd(), "conf")

TESTFILE = os.path.join(BASECONFDIR, "testSetting.conf")

LOGFILE = os.path.join(os.getcwd(), "log", "chilwater.log")
LOGLEVEL = logging.INFO
