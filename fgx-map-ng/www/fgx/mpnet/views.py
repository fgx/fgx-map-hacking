
from django.views.decorators.cache import never_cache
from django.core.cache import cache

import settings
import helpers as h
from mpnet import mp_telnet

"""

@module.route('/flights')
def flights():
	
	#Fetches the latest flights from upstream, fgx-mpstatus-bot
	#return an error if the call is unsuccesful
	#TODO maybe return return "last memcached ?
	
	payload = {'success': True}
	
	req = urllib2.Request("http://localhost:8099/ajax/mpservers")
	try:
		req.urlopen(req)
	except:
		print "FAIL", req
	return Foo

	@module.route('/ajax/mpservers')

def mpservers():
	
	#Fetches the latest list of MPservers from upstream, fgx-mpstatus-bot
	#return an error if the call is unsuccesful
	#TODO maybe return return "last memcached ?
	
	payload = {'success': True}
	

	#req = urllib2.Request("http://localhost:8099/ajax/mpservers")
	#try:
	#	req.urlopen(req)
	#except:
	#	print "FAIL", req

	
	#entries = H2.query.all()c
	return jsonify(payload)

	
"""	

@never_cache
@h.render_to_json()
def flights(request):
	
	dic = dict(success=True, flights=None)
	
	## If we got a custom server then its a manual call
	server = request.GET.get('server')
	if server:
		i = h.to_int(server)
		if i > 0:
			server = "mpserver%02d.flightgear.org" % i
		reply =  mp_telnet.fetch_telnet(server, False)
		if not reply.error:
			dic['flights'] = reply.flights
		
		
	else:	
		## Were reading from cache
		server = settings.FGX_MP_SERVER
		
		dic['flights'] = cache.get("flights")
		dic['source'] = "memcache"
		dic['last_update'] = cache.get("last_update")

		
	return dic
	