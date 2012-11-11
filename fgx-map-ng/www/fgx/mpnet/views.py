

import urllib2
import json

from flask import render_template, request, jsonify

import settings
import helpers as h
#from mpnet import mp_telnet



from fgx import app
from fgx import cache

def get_crossfeed():
	
	
	#cf_data = None #cache.get("cf_data")
	#if not cf_data:
	req = urllib2.Request('http://cf.fgx.ch/data')
	response = urllib2.urlopen(req)
	cf_data = response.read()
	#print "remote", cf_data
	#cache.set("cf_data", cf_data)
	#workaround
	cf_data =  cf_data[0:-6] + "]}"
	return cf_data
	#return json.loads(cf_data)

@app.route('/ajax/mp/flights/cf', methods=['GET'])
def flights_crossfeed():
	
	data =   get_crossfeed()
	
	#payload = dict(success=True, data=data)
	
	
	
	return data
	

@app.route('/ajax/mp/flights/telnet', methods=['GET'])
def flights_telnet():
	
	payload = dict(success=True, flights=None)
	
	## If we got a custom server then its a manual call
	server = request.args.get('server')
	if server:
		i = h.to_int(server)
		if i > 0:
			server = "mpserver%02d.flightgear.org" % i
		reply =  mp_telnet.fetch_telnet(server, False)
		if not reply.error:
			dic['flights'] = reply.flights
		
		
	else:	
		## Were reading from cache
		#server = settings.FGX_MP_SERVER
		
		payload['flights'] = cache.get("flights")
		payload['source'] = "memcache"
		payload['last_update'] = cache.get("last_update")

		
	return jsonify(payload)
	
	
	