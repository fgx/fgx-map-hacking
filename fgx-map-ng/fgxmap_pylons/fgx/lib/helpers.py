## @package fgx.lib.helpers
# @brief Helper functions

# Consists of functions to typically be used within templates, but also
# available to Controllers. This module is available to templates as {h}.

from pylons import config

def G():
	return config['pylons.app_globals']

## Converts a value to an int, captures the python foo = int(bar) exception and return None instead
# @returns an <b>int</b> if succesful, else <b>None</b>
def to_int(v):
	try:
		i = int(v)
	except ValueError:
		i = None
	return i
	
## Reads a file and return its contents
# @param path to the file as string, preferably absolute
# @retval str with the files contents
def read_file(path):
	f = open(path, "r")
	con = f.read()
	f.close()
	return con

	
####################################################	
## \defgroup helpers_shortcuts Shortcut functions
# The shortucts are used to extract a key and type from a dict

## Returns a value, strings are stripped, and none if zero length string
# @param dic dictionary of values
# @param ki key to find
# @param ret_none False to return <b>None</b> instead of zero length string
# @return <b>zero</b> or <b>None</b>
# \ingroup helpers_shortcuts
def v(dic, ki, ret_none=True):
	"""Return the value from request.params or None if key not exist"""
	if not ki in dic.params:
		return None
	va =  dic.params[ki]
	if isinstance(va, str) or isinstance(va, unicode):
		vs = va.strip()
		if ret_none:
			if len(vs) == 0:
				return None
		return vs		
	return va
	
## Helper to get integer
# @param dic dictionary of values
# @param ki Key to find
# @param null_zeros True to return None instead of zero
# @return <b>zero</b> or <b>None</b>
# \ingroup helpers_shortcuts
def i(dic, ki, null_zeros=False):
	vv = v(dic, ki)
	if vv == None:
		return None
	ival =  to_int(vv)
	if null_zeros and ival == 0:
		return None
	return ival
		
## Helper to get boolean, attempt to falsify "", "false", "0" and "off"
# @param dic dictionary of values
# @param ki Key to find
# @return <b>1</b> or <b>None</b>
# \ingroup helpers_shortcuts
def b(dic, ki):
	
	if not ki in dic.params:
		return None
	s = str(dic.params[ki]).strip()
	if s == "" or s == "0" or s == "off" or s == "true":
		return None
	return 1
	
	
	
	