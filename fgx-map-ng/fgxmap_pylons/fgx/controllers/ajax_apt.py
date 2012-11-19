import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from sqlalchemy import or_

from fgx.lib.base import BaseController, render

from fgx.lib.base import BaseController, render
from fgx.model import meta, Airport

log = logging.getLogger(__name__)

class AjaxAptController(BaseController):

	@jsonify
	def airports(self):
	
		payload = {'success': True}

		q = request.params['q'].upper()
			
		obs = meta.Session.query(Airport).filter(Airport.apt_ident.contains(q)).limit(100).all()
			
		payload['airports'] = [ob.dic() for ob in obs]
			
	
		return payload
