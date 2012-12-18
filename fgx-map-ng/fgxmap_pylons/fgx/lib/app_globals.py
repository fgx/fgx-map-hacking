"""The application's Globals object"""

import os
import glob
import random

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options


class Globals(object):
	"""Globals acts as a container for objects available throughout the
	life of the application

	"""

	def __init__(self, config):
		"""One instance of Globals is created during application
		initialization and is available during requests via the
		'app_globals' variable

		"""
		self.root_path = os.path.abspath(os.path.dirname(__file__) + "/../"  )
		
		self.cache = CacheManager(**parse_cache_config_options(config))

		self.crossfeed_data_url = config['crossfeed_ajax_url']
		
		self.temp_dir = config['temp_dir']
		
		## This is the version used on javascript=/fgx_js.X/* ,,
		## Js is send cached, so new change means incrementing this number and directory rename
		## This searched for fgx_js.X/ and sets the fgx_js_versin to X
		path =  glob.glob(self.root_path + '/public/fgx_js.[0-9].[0-9]/')[0]
		self.fgx_js_version =  path.split("/")[-2].replace("fgx_js.", "")
		
		
		
	@property
	def static_url(self):
		#return "http://127.0.00.1/~fgxx/fgx-static/"
		return "http://static.fgx.ch"
		
	
