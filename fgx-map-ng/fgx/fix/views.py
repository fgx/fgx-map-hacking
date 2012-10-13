
from django.http import HttpResponse

from fix.models import Fix

from utils import rjson


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