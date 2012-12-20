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
	# Ajax Airports
	##=======================================================================
	
	# Airports
	map.connect('/ajax/airports/icao/{a1}/{a2}/{a3}/{a4}', controller="ajax_airports", action="airports_icao")
	map.connect('/ajax/airports/icao/{a1}/{a2}/{a3}', controller="ajax_airports", action="airports_icao")
	map.connect('/ajax/airports/icao/{a1}/{a2}', controller="ajax_airports", action="airports_icao")
	map.connect('/ajax/airports/icao/{a1}', controller="ajax_airports", action="airports_icao")
	
	map.connect('/ajax/airports', controller="ajax_airports", action="airports")
	map.connect('/ajax/airport/{apt_ident}', controller="ajax_airports", action="airport")
	map.connect('/ajax/airport/{apt_ident}/metar', controller="ajax_airports", action="airport_metar")
	map.connect('/ajax/airport/{apt_ident}/tree', controller="ajax_airports", action="airport_tree")
	
	# Airway
	map.connect('/ajax/airways', controller="ajax_navaids", action="airways")
	map.connect('/ajax/airway/{awy}', controller="ajax_navaids", action="airway")

	
		
	##=======================================================================
	# Ajax Database
	##=======================================================================
	map.connect('/ajax/dev/databases', controller="ajax_dev", action="databases")
	
	map.connect('/ajax/dev/database/{db_name}/tables', controller="ajax_dev", action="tables")
	map.connect('/ajax/dev/database/{db_name}/table/{table_name}/columns', controller="ajax_dev", action="columns")
	map.connect('/ajax/dev/database/{db_name}/table/{table_name}/drop', controller="ajax_dev", action="drop_table")
	
	map.connect('/ajax/dev/routes', controller="ajax_dev", action="routes")
	
	##=======================================================================
	# Layers
	##=======================================================================
	
	map.connect('/ajax/map/layers', controller="ajax_layers", action="layers_index")
	map.connect('/ajax/map/layers/tilecache.cfg', controller="ajax_layers", action="tilecache_cfg")
	map.connect('/ajax/map/layers/resources.xml', controller="ajax_layers", action="resources_xml")
	
	

	##=======================================================================
	# Ajax MultiPlayer
	##=======================================================================
	# MultiPlayer
	map.connect('/ajax/mpnet/status', controller="ajax_mpnet", action="mpstatus")
	
	map.connect('/ajax/bots', controller="ajax_mpnet", action="bots")
	map.connect('/ajax/bot/{bot_name}/{bot_action}', controller="ajax_mpnet", action="bot")
	
	map.connect('/ajax/mpnet/flights/crossfeed', controller="ajax_mpnet", action="crossfeed")
	map.connect('/ajax/mpnet/flights/telnet/{server}', controller="ajax_mpnet", action="telnet")
	map.connect('/ajax/mpnet/flights', controller="ajax_mpnet", action="flights")
		
	
	##=======================================================================
	# Ajax Navaids
	##=======================================================================
	# Nav Aids
	map.connect('/ajax/navaids', controller="ajax_navaids", action="navaids")
	
	map.connect('/ajax/fix/{ident}', controller="ajax_navaids", action="fix")
	map.connect('/ajax/fix', controller="ajax_navaids", action="fix")
	
	map.connect('/ajax/ndb/{ident}', controller="ajax_navaids", action="ndb")
	map.connect('/ajax/ndb', controller="ajax_navaids", action="ndb")
	
	map.connect('/ajax/vor/{ident}', controller="ajax_navaids", action="vor")
	map.connect('/ajax/vor', controller="ajax_navaids", action="vor")
	
	map.connect('/ajax/flightplan/process', controller="ajax_navaids", action="process_flightplan")
	
	##=======================================================================
	# Ajax Users
	##=======================================================================
	### Secure
	map.connect('/ajax/users', controller="ajax_users", action="users")
	map.connect('/ajax/user/{user_id}', controller="ajax_users", action="user")
	
	
	
	##=======================================================================
	## HTML Pages
	##=======================================================================
	## The css for icons
	map.connect('/dynamic.{fgx_ver}.css', controller='html_pages', action="dynamic_icons_css")
	
	# TODO
	map.connect('/admin/users', controller="html_pages", action="admin_users")
	
	map.connect('/{page}', controller="html_pages", action="index")
	map.connect('/', controller="html_pages", action="index")
	
	return map
