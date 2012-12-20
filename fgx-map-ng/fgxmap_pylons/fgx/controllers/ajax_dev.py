##@package fgx.controllers.ajax_dev
# @brief Developer utils controllers and helpers
#

import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify
from pylons import config

from fgx.lib.base import BaseController, render
from fgx.model import meta
from fgx.queries import database

log = logging.getLogger(__name__)



class AjaxDevController(BaseController):

	####
	## @brief Returns a list of tables
	#
	# @see queries.database.tables()
	# 
	# @param db_name database connection
	@jsonify
	def db_tables(self, db_name):

		payload = dict(
					success=True,
					tables = database.tables(db_name)
				)
		
		return payload

	####
	## @brief Returns a list of column definitions in a table in json
	#
	# @see queries.database.columns()
	# 
	# @param db_name database connection
	# @param table_name The table to query columns for
	@jsonify	
	def db_columns(self, db_name, table_name):
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
	
	####
	## @brief Update and create database views
	# @todo This needs to be implemented - pete
	#
	# The idea is to create the views here, so updates are easy. Requires create view permission.
	@jsonify	
	def create_views(self):
		
		payload = dict(success=True)
		views_sql = []
		
		## v_runway
		sql = "TODOcreate or replace view v_runway as "
		sql += "select apt_ident, rwy_ident, rwy_ident_end, "
		sql += " rwy_ident || '-' || rwy_ident_end as rwy "
		sql += " from runway "
		views_sql.append(sql)
		
		
		## Create views
		for s in views_sql:
			meta.Sess.data.execute(s)
		
		payload['views'] = views_sql
		
		return payload
		
		
		
	## @brief Returns a list raw routes defined in fgx.config.routing, url: /ajax/dev/routes
	# @return list with dic 
	@jsonify
	def routes(self):
		
		lst = []
		for r in config['routes.map']._routematches:
			#print dir(r)
			lst.append( {	'url': r.routepath, 
							"controller": r._kargs['controller'] if 'controller' in r._kargs else None,
							"action": r._kargs['action'] if 'action' in r._kargs else None
							} )
		payload = dict(	success=True, routes = sorted(lst) )

		return payload
	
	
	
