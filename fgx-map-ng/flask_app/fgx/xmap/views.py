from flask import render_template, request

from xmap import module

class Context(object):
	pass

	
@module.route('/')
def index():
	c = Context()
	c.remote_addr = request.environ['REMOTE_ADDR']
	c.static_url = "http://static.fgx.ch"
	return render_template('sxmap/index.html', c=c)

	