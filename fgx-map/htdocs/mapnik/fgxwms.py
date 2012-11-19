#!/usr/bin/env python

# (c) 2011 Yves Sablonier, Zurich, Licence: GNU GPLv2
# Do not remove this copyright notice !

# Code based on core and examples provided by Dane Springmeyer & Co.
# at the famous Mapnik2 project: http://code.google.com/p/mapnik-utils/
# Abstract: OGCServer provides a Mapnik WMS server for your data

import sys
sys.path.append('/home/map/fgx-map/fgx-map/wmsserver')

from ogcserver.cgiserver import Handler
from jon import fcgi

class OGCServerHandler(Handler):
    configpath = '/home/map/fgx-map/fgx-map/wmsserver/ogcserver.conf'

fcgi.Server({fcgi.FCGI_RESPONDER: OGCServerHandler}).run()
