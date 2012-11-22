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

class AjaxAirportsController(BaseController):

	@jsonify
	def airports(self):
	
		payload = {'success': True}

		apt_ident = h.v(request, "apt_ident")
		apt_name_ascii = h.v(request, "apt_name_ascii")
		bounds = h.v(request, "bounds")
		
		if apt_ident or apt_name_ascii or bounds:
			payload['airports'] = airports.airports(
											apt_ident=apt_ident, 
											apt_name_ascii=apt_name_ascii, 
											bounds=bounds)
		
		else:
			payload['error'] = "Need a ?search  or ?bounds "
			payload['aiports'] = []
			
		return payload
		
		
		
	@jsonify
	def airport(self, apt_ident):
	
		payload = {'success': True}

		
		
		payload['airport'] = airports.airport(apt_ident)
		#payload['airport'] = airports.airport(apt_ident)
		payload['runways'] = airports.runways(apt_ident)
			
		return payload

