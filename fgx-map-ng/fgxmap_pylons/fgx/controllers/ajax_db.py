import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from fgx.lib.base import BaseController, render
from fgx.model import meta
from fgx.queries import database

log = logging.getLogger(__name__)



class AjaxDbController(BaseController):

	@jsonify
	def tables(self, db_name):

		payload = dict(
					success=True,
					tables = database.tables(db_name)
				)
		
		return payload
		
	@jsonify	
	def columns(self, db_name, table_name):
		payload = dict(
					success=True,
					columns=database.columns(db_name, table_name)
				)
		
		return payload
		
	"""	
	@jsonify
	def drop_table(self, table):
		
		payload = dict(
					success=True
		)
		#Base.metadata.drop_all(bind=Session.bind)
		database.drop_table(table)
		return payload
	"""
	
	def create_views(self):
		
		views = []
		
		sql = "create or replace view v_runway as "
		sql += "select apt_ident, rwy_ident, rwy_ident_end, "
		sql += " rwy_ident || '-' || rwy_ident_end as rwy,"
		sql += " from airport "
		
		
		
		
	
	
