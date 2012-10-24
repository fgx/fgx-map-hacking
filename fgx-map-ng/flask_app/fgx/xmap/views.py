

from flask import render_template, request

from fgx import app

class Context(object):
	pass

	
@app.route('/')
def index():
	c = Context()
	c.remote_addr = request.environ['REMOTE_ADDR']
	c.static_url = "http://static.fgx.ch"
	return render_template('map-ext.html', c=c)

	