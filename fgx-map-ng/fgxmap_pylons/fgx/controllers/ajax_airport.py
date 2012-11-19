import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from sqlalchemy import or_

from fgx.lib.base import BaseController, render

from fgx.lib import helpers as h
from fgx.model import meta, Airport
from fgx.queries import airports

log = logging.getLogger(__name__)

class AjaxAirportController(BaseController):

	@jsonify
	def airports(self):
	
		payload = {'success': True}

		search = h.v(request, "search")
		bounds = h.v(request, "bounds")
		
		if search or bounds:
			payload['airports'] = airports.airports(search=search, bounds=bounds)
		
		else:
			payload['error'] = "Need a ?search  or ?bounds "
			payload['aiports'] = []
			
			
		
			
	
		return payload
