
from xplane import server
from utils import render_to_json

@render_to_json()
def avail(request):
	
	dic = dict(success=True)
	
	dic['files'] = server.get_remote_list()
	
	
	return dic
	
	
