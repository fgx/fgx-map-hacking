
from django.http import HttpResponse
from django.contrib.gis.gdal.envelope import Envelope


from models import Fix
import helpers as h
import queries

#W = 39.9; N = -82.9; E=40.4; S=-82.2
#bounds = Envelope((N, W, S, E, ))
#Base.objects.filter(location__intersects=bounds.wkt)

## This is called as /fix?search=foo and /fix/<ident>

@h.render_to_json()
def fix_models_version(request, ident=None):
	
	## We got an ident , ie sungular
	if ident:
		obs = Fix.objects.filter(fix=ident)[:10]	
	
	else:
		## get the ?search=Foo
		search = request.GET.get("search")

		if search:
			
			
			
			## Get the fix ojects _icontains == insensitive ==  ilike '%foo%' in sql limit to 100
			obs = Fix.objects.filter(fix__icontains=search)[:100]	
			
			
			#sprint 
		else:
			obs = []
	
	##  loop the objects to a list, calling getting the dic() for each object
	fix_data_list = [ o.dic() for o in obs ]
	
	## Make return payload 
	payload = dict(fix=fix_data_list, success=True)
	
	## This is encoded to json by @h.render_to_json()
	return payload

@h.render_to_json()
def fix(request, ident=None):
	
	search = request.GET.get("search")

	payload = dict(success=True)
	
	if search:
		
		payload['fix_data'] = queries.fix(search=search)
		
		
	
	return payload
	
	