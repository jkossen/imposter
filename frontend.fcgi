#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from frontend import app

WSGIServer(app, bindAddress=app.config['FRONTEND_FCGI_SOCKET']).run()
