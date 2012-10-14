


from django.shortcuts import render_to_response

from utils import make_context



## Show Index page
def index(request):
	
	c = make_context()

	
	return render_to_response('index.html', {'c': c})	


## Show Map page
def map(request, map_name):
	
	c = make_context()
	
	return render_to_response('map-%s.html' % map_name, {'c': c})	
