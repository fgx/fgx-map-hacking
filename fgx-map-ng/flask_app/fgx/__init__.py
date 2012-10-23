import json, os, re, sys

from flask import Flask
#from pytz.gae import pytz # NOTE: Import gae.pytz before Babel!!!
#from flaskext.babel import Babel
from flask.ext.cache import Cache
#from flaskext.debugtoolbar import DebugToolbarExtension
from flask.ext.sqlalchemy import SQLAlchemy
#from repoze.browserid.middleware import BrowserIdMiddleware
#from werkzeug.contrib.securecookie import SecureCookie

#from . import filters

__all__ = ['create_app', 'db'] #, 'cache']


# A list of app modules and their prefixes. Each APP entry must contain a
# 'name', the remaining arguments are optional. An optional 'models': False
# argument can be given to disable loading models for a given module.
NOT_USED_MODULES = [
	#{'name': 'airports',  'url_prefix': '/'},
	#{'name': 'navaids',  'url_prefix': '/'},
	
	{'name': 'dbase', 'url_prefix': '/'},
	#{'name': 'mpservers', 'url_prefix': '/'},
	{'name': 'xmap', 'url_prefix': '/'},
	#{'name': 'mod3', 'url_prefix': '/scenery'  },
]

# Create the app
def create_app(name = __name__):
	
	app = Flask(__name__, static_path='/static', template_folder='templates')
	
	app.config.from_object(__name__)
	app.config.from_object('settings')
	app.config.from_envvar('SKELETON_SETTINGS', silent=True)
	
	
	#babel.init_app(app)
	cache.init_app(app)
	db.init_app(app)
	
	#filters.init_app(app)
	register_local_modules(app)

	app.wsgi_app = ProxyFixupHelper(app.wsgi_app)

	#print db, cache
	# Enable the DebugToolbar
	if app.config['DEBUG_TOOLBAR']:
		toolbar = DebugToolbarExtension(app)


	return app



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


def register_local_modules(app):
	#cur = os.path.abspath(__file__)
	#sys.path.append(os.path.dirname(cur) + '/modules')
	#sys.path.append(os.path.dirname(cur) + '/') # pete moving from subdir
	
	## dbase
	from dbase.views import mod as dbaseModule
	app.register_blueprint(dbaseModule)
	
	
	## navaids
	from navaids.views import mod as navaidsModule
	app.register_blueprint(navaidsModule)
	from navaids import models
	
	## xmap
	from xmap.views import mod as xmapModule
	app.register_blueprint(xmapModule)
  
	

		
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
		
##############################################################
# Flask Extensions
#babel = Babel() << for later said peteffs
cache = Cache() #<< for later said peteffs


# Models are added to the db's metadata when create_app() is actually called.
db = SQLAlchemy()


