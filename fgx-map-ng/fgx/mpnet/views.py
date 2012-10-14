
from django.views.decorators.cache import never_cache

import helpers as h

from mpnet import mp_telnet


@never_cache
@h.render_to_json()
def flights(request):
	
	dic = dict(success=True)
	
	server = request.GET.get('server')
	dic['ssss'] = server
	if server:
		i = h.to_int(server)
		if i > 0:
			server = "mpserver%02d.flightgear.org" % i
	else:	
		server = settings.FGX_MP_SERVER
		
		
	dic['server'] = server
	
	
	lag, dic['flights'] = mp_telnet.fetch_telnet(server, False)
	
	
	return dic
	