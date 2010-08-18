#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from admin import app

WSGIServer(app).run()
