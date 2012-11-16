import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from fgx.lib.base import BaseController, render

from fgx.queries import database

log = logging.getLogger(__name__)



class AjaxDbController(BaseController):

	@jsonify
	def tables(self):

		payload = dict(
					success = True,
					tables = database.tables()
				)
		
		return payload
		
	@jsonify	
	def columns(self, table):
		payload = dict(
					success = True,
					columns = database.columns(table)
				)
		
		return payload
		
