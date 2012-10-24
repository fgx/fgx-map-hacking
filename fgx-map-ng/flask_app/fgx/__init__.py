import json, os, re, sys

from flask import Flask
#from pytz.gae import pytz # NOTE: Import gae.pytz before Babel!!!


from flask.ext.cache import Cache
from flask.ext.sqlalchemy import SQLAlchemy

#from flaskext.debugtoolbar import DebugToolbarExtension



#__all__ = ['create_app', 'db'] #, 'cache']

	
app = Flask(__name__, static_path='/static', template_folder='templates')

app.config.from_object(__name__)
app.config.from_object('settings')
app.config.from_envvar('SKELETON_SETTINGS', silent=True)
	
	
cache = Cache() 
cache.init_app(app)

db = SQLAlchemy()
db.init_app(app)

#################################################################
## Import all the views as models so they are registered on load

import dbase.views

import navaids.views
import navaids.models

import xmap.views





# Enable the DebugToolbar
if app.config['DEBUG_TOOLBAR']:
	toolbar = DebugToolbarExtension(app)





# Load the local modules
def load_module_models(app, module):
	if 'models' in module and module['models'] == False:
		print "out ########?"
		return

	name = module['name']
	if app.config['DEBUG']:
		print "[MODEL] Loading db model '%s'" % (name)
	model_name = '%s.models' % (name)
	try:
		mod = __import__(model_name, globals(), locals(), [], -1)
	except ImportError as e:
		if re.match(r'No module named ', e.message) == None:
			print '[MODEL] Unable to load the model for %s: %s' % (model_name, e.message)
		else:
			print '[MODEL] Other(%s): %s' % (model_name, e.message)
		return False
	return True


  
	

		
	"""
		#for m in MODULES:
		print ">> %s " % m['name']
		mod_name = '%s.views' % m['name']
		print "  import mod=" + mod_name
		#views = __import__(mod_name, globals(), locals(), [], -1)
		try:
			views = __import__(mod_name, globals(), locals(), [], -1)
			print "VIEWS=", views.module
		except ImportError:
			print "import error", m
			load_module_models(app, m)
		else:
			url_prefix = None
			if 'url_prefix' in m:
				url_prefix = m['url_prefix']

			if app.config['DEBUG']:
				print '[VIEW ] Mapping views in `%s` to prefix: %s' % (mod_name, url_prefix)

			# Automatically map '/' to None to prevent modules from
			# stepping on one another.
			if url_prefix == '/':
				url_prefix = None
			load_module_models(app, m)
			app.register_module(views.module, url_prefix=url_prefix)

	"""
# Seeing 127.0.0.1 is almost never correct, promise.  We're proxied 99.9% of
# the time behind a load balancer or proxying webserver. Pull the right IP
# address from the correct HTTP header. In my hosting environments, I inject
# X-Real-IP as the HTTP header of choice instead of appending to
# X-Forwarded-For. Mixing and matching HTTP headers used by a client's proxy
# infrastructure and the server's infrastructure is almost always a bad idea.
class ProxyFixupHelper(object):
	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		# Only perform this fixup if the current remote host is localhost.
		if environ['REMOTE_ADDR'] == '127.0.0.1':
			host = environ.get('HTTP_X_REAL_IP', False)
			if host:
				environ['REMOTE_ADDR'] = host
		return self.app(environ, start_response)

app.wsgi_app = ProxyFixupHelper(app.wsgi_app)



