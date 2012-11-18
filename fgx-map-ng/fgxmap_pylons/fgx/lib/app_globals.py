"""The application's Globals object"""

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
		

		#FGX_MP_SERVER = "mpserver14.flightgear.org"
		#fgx_ = "217.150.241.103"
		
	@property
	def static_url(self):
		# Later this will be a selection of servers of random(x, y, x) if busy
		return "http://static.fgx.ch"
		#return "http://fgx-static.freeflightsim.org"
		
	
