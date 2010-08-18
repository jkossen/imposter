#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from frontend import app

WSGIServer(app).run()
