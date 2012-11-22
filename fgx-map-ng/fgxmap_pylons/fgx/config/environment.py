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
from fgx.bots.mpstatus import MpStatusThread
from fgx.bots.tracker import TrackerThread

def load_environment(global_conf, app_conf, start_bots):
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
	

	# Create the Jinja2 Environment
	config['pylons.app_globals'].jinja2_env = Environment(
							#extensions=[jinja_ext], 
							loader=ChoiceLoader(
								[FileSystemLoader(path) for path in paths['templates']],
							)
	)
	
	# Setup the SQLAlchemy database engine
	class Engines(object):
		pass
	engines = Engines()
	engines.data = engine_from_config(config, 'sql_data.')
	engines.secure = engine_from_config(config, 'sql_secure.')
	engines.mpnet = engine_from_config(config, 'sql_mpnet.')
	
	init_model(engines)

	# CONFIGURATION OPTIONS HERE (note: all config options will override
	# any Pylons config options)
	
	
	
	##====================================================
	## Start the background processes
	if start_bots:
		#pass
		statusThread = MpStatusThread(config=config)
		statusThread.start()
		
		trackerThread = TrackerThread(config=config)
		trackerThread.start()

	return config
