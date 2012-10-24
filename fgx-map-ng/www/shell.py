#!/usr/bin/env python

## attempt at loading flask app env with shell

import os, sys
xpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))  
if not xpath in sys.path:
	sys.path.insert(0, xpath)
	print "  > Appended in www/__init__", xpath
	


## import and create app
from fgx import app


## Beacuse we are not in wsgi, we need to create a "fake" request context
ctx = app.test_request_context()
ctx.push()

## No import the db
#from fgx import db
#ses = db.session



