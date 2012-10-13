
from django.http import HttpResponse
from django.contrib.gis.gdal.envelope import Envelope


from fix.models import Fix
from utils import rjson

#W = 39.9; N = -82.9; E=40.4; S=-82.2
#bounds = Envelope((N, W, S, E, ))
#Base.objects.filter(location__intersects=bounds.wkt)

@rjson(indent=2)
def fix(request, ident=None):
	
	## We got an ident
	if ident:
		obs = Fix.objects.filter(fix=ident)[:10]	
	
	else:
		q = request.GET.get("q")
		#print q
		if q:
			obs = Fix.objects.filter(fix__contains=q)[:100]	
			#sprint 
		else:
			obs = []
	
	
	data = [ o.dic() for o in obs ]
	
	dic = dict(fix=data, success=True)
	
	return dic
	
	return HttpResponse( dic )
	
	
	