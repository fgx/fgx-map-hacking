##@package fgx.controllers.ajax_map
# @brief Map related controllers and functions
#
import logging
import ConfigParser
from bs4 import BeautifulSoup

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from fgx.lib.base import BaseController, render
from fgx.model import meta
from fgx.lib import helpers as h

log = logging.getLogger(__name__)
 
## Hack that returns ini files as a dictionary. Why this is not in py ?
#
# http://stackoverflow.com/questions/3220670/read-all-the-contents-in-ini-file-into-dictionary-with-python/3220891#3220891
class FGxConfigParser(ConfigParser.ConfigParser):

	## Retrieve ini file as dictionary
	# @retval dict with the contents as section/values
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d

		
        
## Reads and returns the ``tilecache.cfg`` in this project
# @retval str raw contents as string
# @retval dict contents as section/values
def load_tilecache_cfg():
	file_path = h.G().root_path + "/../../tilecache/tilecache.cfg" 
		
	raw = h.read_file( file_path )
	
	parser = FGxConfigParser()
	parser.read(file_path)

	dic =  parser.as_dict()
	del dic['cache']
		
	return {'raw': raw, 'layers': dic }

## Reads and returns the ``tilecache.cfg`` in this project
# @retval raw String with contents as string
# @retval layers Dictionary with keys as layers containing data
def load_resources_xml():
	
	## get the raw source contents
	file_path = h.G().root_path + "/../../mapnik/resources.xml" 
	raw = h.read_file( file_path )
	
	## create Beautiful soup object
	soup = BeautifulSoup(raw)
	
	## Find <layer> and <Style> tags (note lower case)
	layer_tags = soup.find_all("layer")
	style_tags = soup.find_all("style")
	
	## Return list of layers
	layers = {}
	for l in layer_tags:
		
		## Get the paramater tags and loop them
		p_tags = l.datasource.find_all("parameter")
		param_tags = {'type': None}
		for p in p_tags:
			## Ignore the database connections
			if not p['name'] in ["host", "port", "dbname", "user", "password"]:
				param_tags[ p['name'] ] = p.contents[0]
		## update the type
		typ = param_tags['type']				
		
		## Get stylename and load style_xml
		stylename = l.stylename.contents[0]
		stylexml = None
		for s in style_tags:
			if s['name'] == stylename:
				stylexml = str(s)
		
		layers[ l['name'] ] = {"name": l['name'], "type": typ, "mapnik_params": param_tags,
								"stylename": stylename, 'stylexml': stylexml
								}
	return {"raw": raw, "layers": layers}

def layers_data():
	
	tile_dic = load_tilecache_cfg()['layers']
	mapnik_dic = load_resources_xml()['layers']
	
	
	## First make up the layers dict with blank record
	blank = {	'layer': None, "type": None,
				'tilecache': None, 'tilecache_params': None, 'levels': None, "metabuffer": None, 'resolutions': None,
				'mapnik': None, "stylename": None, 'stylexml': None, 'mapnik_params': None
				}
	layers = {}
	
	for dk in tile_dic.keys():
		k = dk.upper()
		layers[k] = blank.copy()
		layers[k]['layer'] = k
	
	for dk in mapnik_dic.keys():
		k = dk.upper()
		layers[k] = blank.copy()
		layers[k]['layer'] = k
	
	
	for l in tile_dic:
		
		lu = l.upper()
		#Note: keys and forced lowercase, eg 'metaBuffer' becomes 'metabuffer'
		layers[lu]['tilecache'] = l
		for ki in ["levels", "metabuffer"]:
			layers[lu][ki] = tile_dic[l][ki] if ki in tile_dic[l] else None
		params = {}
		for ki in sorted(tile_dic[l].keys()):
			params[ki] = tile_dic[l][ki]
		layers[lu]['tilecache_params'] = params
		
	for l in mapnik_dic:
		lu = l.upper()
		layers[lu]['mapnik'] = l
		for ki in ["type", "stylename", "stylexml", "mapnik_params"]:
			layers[lu][ki] = mapnik_dic[l][ki] if ki in mapnik_dic[l] else None
	
	return layers
	
############################################
class AjaxMapController(BaseController):

	## Returns a list of layers (the sections from tilecache.cfg)
	@jsonify
	def layers_index(self):
	
		
		payload = dict(	success=True, layers = layers_data().values()	)
	
		return payload

	## Return the details of a layer
	@jsonify
	def layer_details(self, layer):
	
		tile_str, tile_dic = load_tilecache_cfg()
		xml_str, xml_dic = load_resources_xml()
		
		lay_data  =  layers_data()[layer]
			
		payload = dict(	success=True, 
						data = lay_data
						)
	
		return payload
	
	## Returns tilecache_cfg as string and object
	@jsonify
	def tilecache_cfg(self):

		source_string, dic = load_tilecache_cfg()
	
		payload = dict(
					success=True,
					source_string = source_string,
					data = dic
				)
				
		return payload

	## Returns resources.xml as string and object
	@jsonify
	def resources_xml(self):

		source_string, dic = load_resources_xml()
		#TODO
		payload = dict(
					success=True,
					source_string = source_string,
					data = dic
				)
				
		return payload
		