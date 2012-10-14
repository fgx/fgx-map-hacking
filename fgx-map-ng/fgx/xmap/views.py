


from django.shortcuts import render_to_response

import helpers as h



## Show Index page
def index(request):
	
	c = h.make_context()

	
	return render_to_response('index.html', {'c': c})	


## Show Map page
def map(request, map_name):
	
	c = h.make_context()
	
	return render_to_response('map-%s.html' % map_name, {'c': c})	
