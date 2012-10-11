#!/usr/bin/env python

# (c) 2011 Yves Sablonier, Zurich, Licence: GNU GPLv2
# Do not remove this copyright notice !

# Code based on core and examples provided by Dane Springmeyer & Co.
# at the famous Mapnik2 project: http://code.google.com/p/mapnik-utils/
# Abstract: OGCServer provides a Mapnik WMS server for your data

# Server looks for ogcserver.conf in the same directory

import os
import sys
from ogcserver.wsgi import WSGIApp

import os
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(WORKING_DIR)
configpath = os.path.join(WORKING_DIR,'ogcserver.conf')

application = WSGIApp(configpath)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('127.0.0.1', 6044, application)
    print "FGx Maptest WMS Server listening on port 6046 ..."
    print "(c) 2011 Yves Sablonier, Zurich, Licence: GNU GPLv2"
    print "based on OGCServer coming from the famous Mapnik Utils"
    print "by Dane Springmeyer and Co."
    print "Please visit http://code.google.com/p/mapnik-utils/"
	
    httpd.serve_forever()
