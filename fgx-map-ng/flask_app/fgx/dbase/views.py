

import datetime

from flask import Blueprint, render_template, request, jsonify
import queries as q



mod = Blueprint('dbase', __name__, url_prefix='/')




##======================================================================
## HTML
@mod.route('/dbase')
def dbase():
	
	 return render_template('dbase/dbase.html')
	




##=================================================================================
## AJAX

##= List databases
@mod.route('/ajax/dbase')
def dbase_databases_ajax():
	
	payload = {'success/': True}
	
	payload['databases'] = q.databases()
	
	return jsonify(payload)



##= List <database> Tables
@mod.route('/ajax/dbase/<database>')
def dbase_tables_ajax(database):
	
	payload = {'success/': True}
	
	payload['tables'] = q.tables(database)
	
	return jsonify(payload)


##= List <database> Tables Columns
@mod.route('/ajax/dbase/<database>/<table>')
def dbase_columns_ajax(database, table):
	
	payload = {'success/': True}
	
	payload['columns'] = q.columns(table)
	
	return jsonify(payload)
	
