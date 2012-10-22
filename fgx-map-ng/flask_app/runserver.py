#!/usr/bin/env python
from fgx import create_app


app = create_app(__name__)

if app.config['DEBUG']:
    app.debug = True


#print app.config['WERKZEUG_OPTS']
app.run(**app.config['WERKZEUG_OPTS'])

