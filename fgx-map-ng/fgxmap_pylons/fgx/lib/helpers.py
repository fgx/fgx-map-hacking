"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from pylons import config

def G():
	return config['pylons.app_globals']

def temp_dir(extra_path=None):
	print config.keys()
	pth =  config['temp_dir']
	if extra_path:
		pth += extra_path
	return pth
	

def foo():
	return "BAR"