#!/usr/bin/env python

from flup.server.fcgi import WSGIServer
from fgx import app

if __name__ == '__main__':
    WSGIServer(app, bindAddress='/var/run/fgx_mapwww_server.sock').run()
    