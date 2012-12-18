
import logging
import ConfigParser

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from fgx.lib.base import BaseController, render
from fgx.model import meta
from fgx.lib import helpers as h

log = logging.getLogger(__name__)



class AjaxLayersController(BaseController):

	@jsonify
	def tilecache_cfg(self):

		raw = h.read_file( h.G().root_path + "/../../tilecache/tilecache.cfg" )
		
	
		payload = dict(
					success=True,
					#raw = raw
				)
		
		return payload
		
	