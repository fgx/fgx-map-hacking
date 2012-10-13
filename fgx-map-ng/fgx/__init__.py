

import settings

class Context(object):
	pass

def make_context():
	
	c = Context()
	c.FGX_STATIC = settings.FGX_STATIC
	
	return c
	