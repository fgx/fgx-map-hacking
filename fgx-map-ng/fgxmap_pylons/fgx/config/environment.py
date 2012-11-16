"""Pylons environment configuration"""
import os

from jinja2 import ChoiceLoader, Environment, FileSystemLoader
from pylons.configuration import PylonsConfig
#from pylons.error import handle_mako_error
from sqlalchemy import engine_from_config

import fgx.lib.app_globals as app_globals
import fgx.lib.helpers
from fgx.config.routing import make_map
from fgx.model import init_model

## FGx add the bots
from fgx.bots import mpstatus

def load_environment(global_conf, app_conf):
	"""Configure the Pylons environment via the ``pylons.config``
	object
	"""
	config = PylonsConfig()
	
	# Pylons paths
	root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	paths = dict(root=root,
				controllers=os.path.join(root, 'controllers'),
				static_files=os.path.join(root, 'public'),
				templates=[os.path.join(root, 'templates')])

	# Initialize config with the basic options
	config.init_app(global_conf, app_conf, package='fgx', paths=paths)

	config['routes.map'] = make_map(config)
	config['pylons.app_globals'] = app_globals.Globals(config)
	config['pylons.h'] = fgx.lib.helpers
	
	# Setup cache object as early as possible
	import pylons
	pylons.cache._push_object(config['pylons.app_globals'].cache)
	

	# Create the Mako TemplateLookup, with the default auto-escaping
	"""
	config['pylons.app_globals'].mako_lookup = TemplateLookup(
		directories=paths['templates'],
		error_handler=handle_mako_error,
		module_directory=os.path.join(app_conf['cache_dir'], 'templates'),
		input_encoding='utf-8', default_filters=['escape'],
		imports=['from markupsafe import escape'])
	"""
	# Create the Jinja2 Environment
	config['pylons.app_globals'].jinja2_env = Environment(
							#extensions=[jinja_ext], 
							loader=ChoiceLoader(
								[FileSystemLoader(path) for path in paths['templates']],
							)
	)
	
	# Setup the SQLAlchemy database engine
	engine = engine_from_config(config, 'sqlalchemy.')
	init_model(engine)

	# CONFIGURATION OPTIONS HERE (note: all config options will override
	# any Pylons config options)

	## Start the background processes
	mpstatus.start_mpstatus_thread()
		
	
	return config
