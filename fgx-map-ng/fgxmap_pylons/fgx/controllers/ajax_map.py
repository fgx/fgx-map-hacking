
import logging
import ConfigParser

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from fgx.lib.base import BaseController, render
from fgx.model import meta
from fgx.lib import helpers as h

log = logging.getLogger(__name__)



## http://stackoverflow.com/questions/3220670/read-all-the-contents-in-ini-file-into-dictionary-with-python/3220891#3220891
class FGxConfigParser(ConfigParser.ConfigParser):

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d

        
def load_tilecache_cfg():
		cfg_file_path = h.G().root_path + "/../../tilecache/tilecache.cfg" 
		
		raw = h.read_file( cfg_file_path )
		
		parser = FGxConfigParser()
		parser.read(cfg_file_path)
		
		return raw, parser.as_dict() 

		
##================================================================
class AjaxMapController(BaseController):

	@jsonify
	def layers_index(self):
	
		source_string, dic = load_tilecache_cfg()
	
		payload = dict(success=True, layers = sorted(dic.keys()) )
	
	
		return payload

	@jsonify
	def tilecache_cfg(self):

		source_string, dic = load_tilecache_cfg()
	
		payload = dict(
					success=True,
					source_string = source_string,
					config = dic
				)
				
		return payload

