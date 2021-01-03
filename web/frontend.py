import cherrypy
import os

import settings
import persistanceLayer

_CONF = persistanceLayer.getWebServerConf(settings.BASECONFDIR)


def validate_password(realm, username, password):
	return (
		username in _CONF["userPasswords"]
		and _CONF["userPasswords"][username] == password
	)


class CWS(object):
	@cherrypy.expose
	def index(self):
		with open(os.path.join(_CONF["baseWebDir"], "index.html")) as f:
			return f.read()

	@cherrypy.expose
	def test(self, test="test"):
		return "Dies ist ein " + test


cherrypy.config.update(
	{"server.socket_host": _CONF["host"], "server.socket_port": _CONF["port"],}
)
cherrypy.quickstart(
	CWS(),
	"/",
	config={
		"/": {
			"tools.auth_basic.on": _CONF["authEnabled"],
			"tools.auth_basic.realm": _CONF["authRealm"],
			"tools.auth_basic.checkpassword": validate_password,
		}
	},
)
