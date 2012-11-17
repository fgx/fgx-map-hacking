"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

## FGx Notes:
# * The FIRST match is the stuff in /public/
# * The FIRST match in the list below is the one processed.
#


def make_map(config):
	"""Create, configure and return the routes Mapper"""
	map = Mapper(directory=config['pylons.paths']['controllers'],
				always_scan=config['debug'])
	map.minimization = False
	map.explicit = False

	# The ErrorController route (handles 404/500 error pages); it should
	# likely stay at the top, ensuring it can always be resolved
	## @todo: pete to make this a custom handler
	map.connect('/error/{action}', controller='error')
	map.connect('/error/{action}/{id}', controller='error')

	
	
	
	##=======================================================================
	# Ajax Routes
	##=======================================================================
	
	#### MultiPlayer
	map.connect('/ajax/mp/status', controller="ajax_mpnet", action="mpstatus")
	
	map.connect('/ajax/mp/flights/crossfeed', controller="ajax_mpnet", action="crossfeed")
	map.connect('/ajax/mp/flights/telnet/{server}', controller="ajax_mpnet", action="telnet")
	map.connect('/ajax/mp/flights', controller="ajax_mpnet", action="flights")
	
	
	
	#### Database Browsing
	map.connect('/ajax/database/tables', controller="ajax_db", action="tables")
	map.connect('/ajax/database/table/{table}/columns', controller="ajax_db", action="columns")
	
	#map.connect('/ajax/*', controller="ajax_db", action="scolumns")
	
	##=======================================================================
	## HTML Pages
	##=======================================================================
	map.connect('/database', controller="html_pages", action="database")
	
	map.connect('/index', controller="html_pages", action="index")
	map.connect('/', controller="html_pages", action="index")
	

	return map
