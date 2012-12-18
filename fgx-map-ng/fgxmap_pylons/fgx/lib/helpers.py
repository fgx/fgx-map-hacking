"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from pylons import config

def G():
	return config['pylons.app_globals']

def to_int(v):
	try:
		i = int(v)
	except ValueError:
		i = None
	return i
	

def read_file(path):
	f = open(path, "r")
	con = f.read()
	f.close()
	return con
	
########################################################################
## Request Params Shortcut
########################################################################
def v(request, ki, ret_none=False):
	"""Return the value from request.params or None if key not exist"""
	if not ki in request.params:
		return None
	va =  request.params[ki]
	if isinstance(va, str) or isinstance(va, unicode):
		vs = va.strip()
		if ret_none:
			if len(vs) == 0:
				return None
		return vs		
	return va

def i(request, ki, null_zeros=False):
	"""Returns an INTEGER"""
	vv = v(request, ki)
	if vv == None:
		return None
	ival =  to_int(vv)
	if null_zeros and ival == 0:
		return None
	return ival
		
	
def b(request, ki):
	"""Return the value from request.params or None if key not exist"""
	if not ki in request.params:
		return None
	s = str(request.params[ki]).strip()
	if s == "" or s == "0" or s == "off":
		return None
	return 1
	
	
	
	