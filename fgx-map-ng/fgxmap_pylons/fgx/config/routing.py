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

	map.connect('/www/dynamic.{fgx_ver}.css', controller='html_pages', action="dynamic_ico_css")
	
	
	##=======================================================================
	# Ajax Routes
	##=======================================================================
	
	# Airports
	map.connect('/ajax/airports', controller="ajax_airport", action="airports")
	map.connect('/ajax/airport/{apt_ident}', controller="ajax_airport", action="airport")
	
	# Database Browsing
	map.connect('/ajax/databases', controller="ajax_db", action="databases")
	map.connect('/ajax/database/{db}/tables', controller="ajax_db", action="tables")
	map.connect('/ajax/database/{db}/table/{table}/columns', controller="ajax_db", action="columns")
	map.connect('/ajax/database/{db}/table/{table}/drop', controller="ajax_db", action="drop_table")
	
	
	# MultiPlayer
	map.connect('/ajax/mp/status', controller="ajax_mpnet", action="mpstatus")
	map.connect('/ajax/mp/flights/crossfeed', controller="ajax_mpnet", action="crossfeed")
	map.connect('/ajax/mp/flights/telnet/{server}', controller="ajax_mpnet", action="telnet")
	map.connect('/ajax/mp/flights', controller="ajax_mpnet", action="flights")
	
	
	# Nav Aids
	map.connect('/ajax/navaids', controller="ajax_navaids", action="navaids")
	
	map.connect('/ajax/fix/{ident}', controller="ajax_navaids", action="fix")
	map.connect('/ajax/fix', controller="ajax_navaids", action="fix")
	
	map.connect('/ajax/ndb/{ident}', controller="ajax_navaids", action="ndb")
	map.connect('/ajax/ndb', controller="ajax_navaids", action="ndb")
	
	map.connect('/ajax/vor/{ident}', controller="ajax_navaids", action="vor")
	map.connect('/ajax/vor', controller="ajax_navaids", action="vor")
	
	

	map.connect('/ajax/users', controller="ajax_users", action="users")
	map.connect('/ajax/user/{user_id}', controller="ajax_users", action="user")
	
	#map.connect('/ajax/*', controller="ajax_db", action="scolumns")
	
	##=======================================================================
	## HTML Pages
	##=======================================================================
	map.connect('/database', controller="html_pages", action="database")
	
	map.connect('/admin/users', controller="html_pages", action="admin_users")
	
	map.connect('/maptest', controller="html_pages", action="maptest")
	map.connect('/index', controller="html_pages", action="index")
	map.connect('/', controller="html_pages", action="index")
	

	return map
