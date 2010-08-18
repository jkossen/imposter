#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from admin import app
import config as cfg

WSGIServer(app, bindAddress=cfg.ADMIN_FCGI_SOCKET).run()
