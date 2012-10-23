

import datetime

from flask import render_template, request, jsonify

from dbase import module
from dbase import queries as q

##======================================================================
## HTML
@module.route('/dbase')
def dbase():
	
	 return render_template('dbase/dbase.html')
	




##=================================================================================
## AJAX

##= List databases
@module.route('/ajax/dbase')
def dbase_databases_ajax():
	
	payload = {'success/': True}
	
	payload['databases'] = q.databases()
	
	return jsonify(payload)



##= List <database> Tables
@module.route('/ajax/dbase/<database>')
def dbase_tables_ajax(database):
	
	payload = {'success/': True}
	
	payload['tables'] = q.tables(database)
	
	return jsonify(payload)


##= List <database> Tables Columns
@module.route('/ajax/dbase/<database>/<table>')
def dbase_columns_ajax(database, table):
	
	payload = {'success/': True}
	
	payload['columns'] = q.columns(table)
	
	return jsonify(payload)
	
