import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from sqlalchemy import or_

from fgx.lib.base import BaseController, render

from fgx.lib.base import BaseController, render
from fgx.model import meta, Airport
from fgx.queries import airport

log = logging.getLogger(__name__)

class AjaxAptController(BaseController):

	@jsonify
	def airports(self):
	
		payload = {'success': True}

		q = h.v(request, "q")
		bounds = h.v(request, "bounds")
		
		if q or bounds:
			payload['airports'] = queries.airports(search=q, bounds=bounds, apt_type="all")
		
		else:
			payload['error'] = "Need a ?search  or ?bounds "
			payload['aiports'] = []
			
			
		
			
	
		return payload
