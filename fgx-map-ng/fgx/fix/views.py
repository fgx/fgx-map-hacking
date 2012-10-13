
from django.http import HttpResponse

from fix.models import Fix

from utils import rjson

@rjson(indent=2)
def fix(request):
	
	obs = Fix.objects.all()[:10]
	
	data = [ o.dic() for o in obs ]
	
	dic = dict(fix=data, success=True)
	
	return dic
	
	return HttpResponse( dic )