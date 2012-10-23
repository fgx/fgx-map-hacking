
from flask import Blueprint, render_template, request

mod = Blueprint('navaids', __name__)


class Context(object):
	pass

	
@mod.route('/ajax/foo')
def index():
	c = Context()
	c.remote_addr = request.environ['REMOTE_ADDR']
	c.static_url = "http://static.fgx.ch"
	return render_template('map-ext.html', c=c)

	