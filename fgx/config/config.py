
import os
import json
import yaml
from string import Template

import fgx.app_global as G
from fgx.maps import layers

## Template form Javascript layer
LAYER_JS_TPL = """    
LAYERS.push( 
    new OpenLayers.Layer.WMS( "$title", 
	"$url", 
	{layers: '$layer', 
	format: '$vars.format',
	transparent: '$vars.transparent'
	},
	{
	visibility: $visibility
	}
));"""
    
## Write out the layers.js file
# @param ln If true creates a symlink to www_static/js/layers.js
def write_js(ln=False):
	
	
	## Get Resolutions
	resos = layers.resolutions()
	
	js_str = "var RESOLUTIONS = %s\n\n" % json.dumps(resos, indent=4)
	

	
	layers_l = layers.layers_list()
	js_str += "var LAYERS = [];\n"
	
	"""
	var fgx_850_fix = new OpenLayers.Layer.WMS( "FIX", 
    "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
        {layers: 'fgx_850_fix', 
        format: 'image/png',
        transparent:'TRUE'
        },
        {
        visibility:false
        }
    );
    """
    
	for d in layers_l:
		s = "LAYERS.push( new OpenLayers.Layer.WMS(\n"
		s += '  "%s",\n  "%s",\n' % ( d['title'], d['url'] )
		s += "  %s,\n" % json.dumps(d['vars']) 
		s += "  %s\n" % json.dumps( {'visibility': d['visibility']} ) 
		s += "));\n"
		#d['format'] = "image/png"
		#d['transparent'] = "TRUE"
		#print d
		#s = Template(LAYER_JS_TPL).substitute(d)
		js_str += s
		
	
		
		
	out_path = "/etc/config.js"	
	G.write_file(out_path, js_str)
		
	if ln:
		ln_path = G.ROOT + "/www_static/js/config.js"
		if os.path.exists( ln_path ):
			os.remove(ln_path)
		os.symlink(G.ROOT + out_path, ln_path)
		
	
## Writes out nginx config
# @ todo by pete
def write_nginx(ln=False):
	
	s = "server: "
	
	out_path = "/etc/nginx.conf"	
	G.write_file(out_path, s)
	
	
## Writes out \b local_config.yaml	
def write_local_config(dic):
	
	s = yaml.dump(dic)
	G.write_file("/local_config.yaml", s)
	
	
	