
import os
from string import Template

import fgx.app_global as G
from fgx.maps import layers

## Template form Javascript layer
LAYER_JS_TPL = """    
LAYERS.push( 
    new OpenLayers.Layer.WMS( "$title", 
	"$url", 
	{layers: '$layer', 
	format: '$format',
	transparent: '$transparent'
	},
	{
	visibility: $format
	}
));"""
    
## Write out the layers.js file
# @param ln If true creates a symlink to www_static/js/layers.js
def write_js(ln=False):
	
	data = layers.layers_list()
	
	js_str = "var LAYERS = []\n"
	
	for d in data:
		d['format'] = "image/png"
		d['transparent'] = "TRUE"
		s = Template(LAYER_JS_TPL).substitute(d)
		js_str += s
		
	out_path = "/etc/layers.js"	
	G.write_file(out_path, js_str)
		
	if ln:
		ln_path = G.ROOT + "/www_static/js/layers.js"
		if os.path.exists( ln_path ):
			os.remove(ln_path)
		os.symlink(G.ROOT + out_path, ln_path)
		
	
	
def write_nginx(ln=False):
	
	s = "server: "
	
	out_path = "/etc/nginx.conf"	
	G.write_file(out_path, s)
	
	