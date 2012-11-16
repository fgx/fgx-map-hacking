

import datetime

from flask import render_template, request, jsonify
import queries as q

from fgx import app



##======================================================================
## HTML
@app.route('/dbase')
def dbase():
	
	 return render_template('dbase.html')
	




##=================================================================================
## AJAX

##= List databases
@app.route('/ajax/dbase')
def dbase_databases_ajax():
	
	payload = {'success': True}
	
	payload['databases'] = q.databases()
	
	return jsonify(payload)



##= List <database> Tables
@app.route('/ajax/dbase/<database>')
def dbase_tables_ajax(database):
	
	payload = {'success': True}
	
	payload['tables'] = q.tables(database)
	
	return jsonify(payload)


##= List <database> Tables Columns
@app.route('/ajax/dbase/<database>/<table>')
def dbase_columns_ajax(database, table):
	
	payload = {'success': True}
	
	payload['columns'] = q.columns(table)
	
	return jsonify(payload)
	
