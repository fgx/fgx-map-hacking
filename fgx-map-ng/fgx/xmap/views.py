


from django.shortcuts import render_to_response


def index(request):
	
	return render_to_response('map-pete.html', {'foo': "bar"})	