
import yaml

import settings


## Converts to int
# @retval None if invalid, else int
def to_int(v):
	try:
		i = int(v)
	except ValueError:
		i = None
	return i
	

#############################################################

def temp_dir(path=None):
	
	if path == None:
		return settings.TEMP_DIR
		
	s = settings.TEMP_DIR
	
	s = s + path
	
	return  s


## Reads file from project relative to ROOT
def read_file(path):
	f = open(path, "r")
	s = f.read()
	f.close()
	return s

## Reads file from project relative to ROOT
def write_file(path, contents):
	f = open(path, "w")
	s = f.write(contents)
	f.close()
	return

	
def write_json(path, data_dic):
	return write_file(path, json.dumps(data_dic))
	
	
## Reads file from project relative to ROOT and return yaml data, or None	
def read_yaml(path):
	s = read_file(path)
	return yaml.load(s)
	
	
######################################################################
## Convenience context object for templating
class Context(object):
	pass

## Create a default Context object
def make_context():
	
	c = Context()
	c.static_url = settings.FGX_STATIC_URL
	
	return c
	
	
	
######################################################################

from functools import wraps
from django.http import HttpResponse
from django.utils import simplejson as json

def render_to_json(**jsonargs):
    """
    Renders a JSON response with a given returned instance. Assumes json.dumps() can
    handle the result. The default output uses an indent of 4.
    
    @render_to_json()
    def a_view(request, arg1, argN):
        ...
        return {'x': range(4)}

    @render_to_json(indent=2)
    def a_view2(request):
        ...
        return [1, 2, 3]

    """
    def outer(f):
        @wraps(f)
        def inner_json(request, *args, **kwargs):
            result = f(request, *args, **kwargs)
            r = HttpResponse(mimetype='application/json')
            if result:
                indent = jsonargs.pop('indent', 4)
                r.write(json.dumps(result, indent=indent, **jsonargs))
            else:
                r.write("{}")
            return r
        return inner_json
    return outer
    
    
