#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from frontend import app
import config as cfg

WSGIServer(app, bindAddress=cfg.FRONTEND_FCGI_SOCKET).run()
