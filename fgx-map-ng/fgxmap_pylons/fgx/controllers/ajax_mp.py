import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from fgx.lib.base import BaseController, render

log = logging.getLogger(__name__)




class AjaxMpController(BaseController):

	@jsonify
	def flights(self):
		payload = dict(success=True, 
						flights=mylib.get_flights_function() )
		return payload
