#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from admin import app

WSGIServer(app, bindAddress=app.config['FCGI_SOCKET']).run()
