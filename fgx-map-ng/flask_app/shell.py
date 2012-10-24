#!/usr/bin/env python


## attempt at loading flask app env with shell

## import and create app
from fgx import app


## Beacuse we are not in wsgi, we need to create a "fake" request context
ctx = app.test_request_context()
ctx.push()

## No import the db
from fgx import db
ses = db.session


##======================================
## create's all tables
db.create_all()

