##@package fgx.controllers.ajax_map
# @brief Map related controllers and functions
#
import logging
import ConfigParser

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from fgx.lib.base import BaseController, render
from fgx.model import meta
from fgx.lib import helpers as h

log = logging.getLogger(__name__)
 
## Hack that returns ini files as a dictionary. Why this is not in py ?
#
# http://stackoverflow.com/questions/3220670/read-all-the-contents-in-ini-file-into-dictionary-with-python/3220891#3220891
class FGxConfigParser(ConfigParser.ConfigParser):

	## Retrieve ini file as dictionary
	# @retval dict with the contents as section/values
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d

## Reads and returns the ``tilecache.cfg`` in this project
# @retval str raw contents as string
# @retval dict contents as section/values
def load_tilecache_cfg():
	cfg_file_path = h.G().root_path + "/../../tilecache/tilecache.cfg" 
	
	raw = h.read_file( cfg_file_path )
	
	parser = FGxConfigParser()
	parser.read(cfg_file_path)
	
	return raw, parser.as_dict() 

		
############################################
class AjaxMapController(BaseController):

	## Returns a list of layers (the sections from tilecache.cfg)
	@jsonify
	def layers_index(self):
	
		source_string, dic = load_tilecache_cfg()
			
		payload = dict(	success=True, 
						layers = [ {"layer": l} for l in sorted(dic.keys())]
						)
	
	
		return payload

	## Returns tilecache_cfg as string and object
	@jsonify
	def tilecache_cfg(self):

		source_string, dic = load_tilecache_cfg()
	
		payload = dict(
					success=True,
					source_string = source_string,
					config = dic
				)
				
		return payload

