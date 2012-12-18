
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

        
class AjaxLayersController(BaseController):

	@jsonify
	def tilecache_cfg(self):

		cfg_file_path = h.G().root_path + "/../../tilecache/tilecache.cfg" 
		
		raw = h.read_file( cfg_file_path )
		
		parser = FGxConfigParser()
		parser.read(cfg_file_path)
	
		payload = dict(
					success=True,
					config = parser.as_dict()
				)
		
		return payload
		
	