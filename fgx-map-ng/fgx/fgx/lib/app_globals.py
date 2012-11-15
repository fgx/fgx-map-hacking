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

		
		static_url = "http://static.fgx.ch"



		#FGX_MP_SERVER = "mpserver14.flightgear.org"
		fgx_ = "217.150.241.103"