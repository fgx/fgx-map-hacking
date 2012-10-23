
import urllib2

from flask import request, jsonify

#from skeleton import cache

from mpservers import module


@module.route('/ajax/mpservers')

def mpservers():
	"""
	Fetches the latest list of MPservers from upstream, fgx-mpstatus-bot
	return an error if the call is unsuccesful
	TODO maybe return return "last memcached ?
	"""
	payload = {'success': True}
	
	"""
	req = urllib2.Request("http://localhost:8099/ajax/mpservers")
	try:
		req.urlopen(req)
	except:
		print "FAIL", req
	"""
	
	#entries = H2.query.all()c
	return jsonify(payload)
