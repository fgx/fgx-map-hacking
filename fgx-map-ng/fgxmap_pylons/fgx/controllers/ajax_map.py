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
	
	return raw, parser.as_dict() 

## Reads and returns the ``tilecache.cfg`` in this project
# @retval str raw contents as string
# @retval dict contents as section/values
def load_resources_xml():
	
	file_path = h.G().root_path + "/../../mapnik/resources.xml" 
	
	raw = h.read_file( file_path )
	
	soup = BeautifulSoup(raw)
	layer_tags = soup.find_all("layer")
	#print layer_tags
	layers = {}
	for l in layer_tags:
		#print "---------------------"
		#print l
		#print "--------"
		#print l.datasource
		p_tags = l.datasource.find_all("parameter")
		typ = None
		for p in p_tags:
			if p['name'] == "type":
				typ = p.contents[0]
		#print "---"
		#print p_tags
		#print "############"
		layers[ l['name'] ] = {"name": l['name'], "type": typ}
	return raw, layers

	
	
############################################
class AjaxMapController(BaseController):

	## Returns a list of layers (the sections from tilecache.cfg)
	@jsonify
	def layers_all(self):
	
		payload = {"success": True}
		#source_string, dic = load_tilecache_cfg()
		payload['tilecache_cfg'], tile_dic = load_tilecache_cfg()
		payload['resources_xml'], xml_dic = load_resources_xml()
		
		layers = {}
		for l in tile_dic:
			if l != "cache":
				lu = l.upper()
				print tile_dic[l]
				layers[lu] = {'layer': lu, 'tilecache': l, 'mapnik': None, "type": None, 
								'levels': tile_dic[l]['levels'] if 'levels' in tile_dic[l] else None,
								'metabuffer': tile_dic[l]['metabuffer'] if 'metabuffer' in tile_dic[l] else None
								}
			
		for l in xml_dic:
			lu = l.upper()
			if not lu in layers:
				layers[lu] = {'layer': l, 'tilecache': None, 'mapnik': l, "type": None, 'levels': None, "metabuffer": None}
			else:
				layers[lu]['mapnik'] = l
			layers[lu]['type'] = xml_dic[l]['type']
				
		
						
		payload['layers'] = layers.values()
			
	
		return payload

	## Return the details of a layer
	@jsonify
	def layer_details(self, layer):
	
		tile_str, tile_dic = load_tilecache_cfg()
		xml_str, xml_dic = load_resources_xml()
		
		lay_data  =  {}
		lay_data['layer'] = layer
		lay_data['tilecache'] = tile_dic[layer]
		lay_data['mapnik'] = xml_dic[layer]
			
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
		