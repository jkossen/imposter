#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from public_api import app

WSGIServer(app, bindAddress=app.config['PUBLIC_API_FCGI_SOCKET']).run()
