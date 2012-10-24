

import urllib2

from flask import request
from flaskext.jsonify import jsonify


from . import module

@module.route('/flights')
def flights():
	"""
	Fetches the latest flights from upstream, fgx-mpstatus-bot
	return an error if the call is unsuccesful
	TODO maybe return return "last memcached ?
	"""
	payload = {'success': True}
	
	req = urllib2.Request("http://localhost:8099/ajax/mpservers")
	try:
		req.urlopen(req)
	except:
		print "FAIL", req
	return Foo
