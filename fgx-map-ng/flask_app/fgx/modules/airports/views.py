

import datetime

from flask import render_template, request, jsonify

##from fgx_data import  cache
from airports import module, queries


##======================================================================
## HTML
@module.route('/airports')
def airports():
	
	 return render_template('airports/index.html', foo="bar")
	
	
##======================================================================
@module.route('/ajax/airports/count')
###@cache.cached(timeout=20, key_prefix="airports_count")
def airports_count():
	"""
	Returns a list of airports
	
	@args =
	apt_icao= < a code to search, two chars on more >
	icao_only=1 - to return only EGLL aiport and skip small ones with Numbers and three chars etc
	
	"""
	payload = {'success': True}
	
	if request.method == "POST":
		
		payload['error'] = "Only GET currently allowed"
		
		
	else:
		
		#r_apt_icao = request.args.get("apt_icao", None)
		
		payload['airports_count'] = queries.airports_count()
	
	
	return jsonify(payload)
	




@module.route('/ajax/airports')
def airports_ajax():

	payload = {'success': True}
	
	apt_icao = request.args.get("apt_icao", None)
	apt_name = request.args.get("apt_name", None)
	icao_only = request.args.get("icao_only", None)
	
	if apt_icao == None and apt_name == None:
		payload['error'] = "Nothing to do try ?apt_icao=bar or ?apt_name=foo"
		
	else:
		if apt_icao != None and len(apt_icao) < 2:
			payload['error'] = "Need more apt_icao characters"
		
		elif apt_name != None and len(apt_name) < 3:
			payload['error'] = "Need more apt_name characters"
			
		else:
			payload['airports'] = queries.airports(apt_icao=apt_icao, apt_name=apt_name)
	
	return jsonify(payload)



@module.route('/ajax/airport/<apt_icao>')
def airport_ajax(apt_icao):

	payload = {'success': True}

	airport =  queries.airport(	apt_icao )
	if airport == None:
		payload['error'] = "Airport '%s' not found" % apt_icao
		
	else:
		payload['aiport'] = airport
		
	
	return jsonify(payload)
	
""" TO db	
@module.route('/ajax/aptdat')
@module.route('/ajax/aptdat/<table>')
def aptdat_ajax(table=None):

	payload = {'success': True}

	payload['tables'] = queries.aptdat_tables()
	
	return jsonify(payload)
"""