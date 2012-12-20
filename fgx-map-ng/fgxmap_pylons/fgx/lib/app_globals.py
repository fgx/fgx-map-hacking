##@package fgx.lib.app_globals
# @brief The application's globals object
#

import os
import glob
import random

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

## Acts as a container for objects available throughout the life of the application
class Globals(object):
	
	## One instance of Globals is created during application
	# 	initialization and is available during requests via the
	# 	'app_globals' variable
	# Some of this stuff is copy of config of ease of use
	def __init__(self, config):
		"""

		"""
		## The root path the the wsgi root, ie where the ini file is
		self.root_path = os.path.abspath(os.path.dirname(__file__) + "/../"  )
		
		## Cache manager object
		self.cache = CacheManager(**parse_cache_config_options(config))

		## The URL for the crossfeed server
		self.crossfeed_data_url = config['crossfeed_ajax_url']
		
		## Location of temp directory
		self.temp_dir = config['temp_dir']
		
		
		path =  glob.glob(self.root_path + '/public/fgx_js.[0-9].[0-9]/')[0]
		
		## FGx symlink vervion
		self.fgx_js_version =  path.split("/")[-2].replace("fgx_js.", "")
		
		
	## Returns the location of the static server
	# @todo make this an ini setting - pete
	@property
	def static_url(self):
		#TODO Below needs to be in ini config
		return "http://static.fgx.ch"
		
	
