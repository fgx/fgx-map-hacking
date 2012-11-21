"""The application's Globals object"""

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
		self.cache = CacheManager(**parse_cache_config_options(config))

		self.crossfeed_data_url = config['crossfeed_ajax_url']
		
		self.temp_dir = config['temp_dir']
		
		## This is the version used on javascript=/fgx_js.X/* ,,
		## Js is send cached, so new change means incrementing this number and directory rename
		self.fgx_js_version = 1
		
		
	@property
	def static_url(self):
		foo = random.sample( ["http://static.fgx.ch", "http://static.freeflightsim.org"], 1)[0]
		#print foo
		return foo
		# Later this will be a selection of servers of random(x, y, x) if busy
		return "http://static.fgx.ch"
		return "http://fgx-static.freeflightsim.org"
		
	
