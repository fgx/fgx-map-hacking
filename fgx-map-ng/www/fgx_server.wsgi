#!/usr/bin/env python

from flup.server.fcgi import WSGIServer
from fgx_data import app

if __name__ == '__main__':
    WSGIServer(app, bindAddress='/tmp/fgx_navdata_server.sock').run()
    