
import os
import json
import yaml
from string import Template

import fgx.app_global as G
from fgx.maps import layers

    
## Write out the layers.js file
# @param ln If true creates a symlink to www_static/js/layers.js
def write_js(ln=False):
	
	js_str = "// This file is autogenerated DO NOT EDIT THIS FILE\n\n"
	
	## Get Resolutions
	resos = layers.resolutions()
	js_str += "var RESOLUTIONS = %s\n\n" % json.dumps(resos, indent=4)
	

	## Write Layers
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
    ## If anyone can think of a better way  than this mashed strings
	for d in layers_l:
		s = "LAYERS.push( new OpenLayers.Layer.WMS(\n"
		s += '  "%s",\n  "%s",\n' % ( d['title'], d['url'] )
		s += "  %s,\n" % json.dumps(d['vars']) 
		s += "  %s\n" % json.dumps( {'visibility': d['visibility']} ) 
		s += "));\n"
		js_str += s
		
	
		
	out_path = "/etc/config.js"	
	G.write_file(out_path, js_str)
		
	if ln:
		ln_path = G.ROOT + "/www_static/js/config.js"
		if os.path.exists( ln_path ):
			os.remove(ln_path)
		os.symlink(G.ROOT + out_path, ln_path)
		
		ln_path = G.ROOT + "/django_app/static/js/config.js"
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
	
	
## Writed out the \b /etc/tilecache.cfg file
def write_tilecache_cgf():
	
	resos = layers.resolutions()
	resos_s = ",".join([ str(r) for r in resos ])
	print resos_s
	
	s = ""
	layers_l = layers.layers_list()
	for l in layers_l:
		
		lst = [
			"[%s]" % l['layer'],
			"url=http://map.fgx.ch:81/mapnik/fgxwms.py?&TRANSPARENT=TRUE&",
			"extension=png",
			"srs=EPSG:3857",
			"levels=20",
			"metaTile=true",
			"metaSize=2,2",
			"metaBuffer=128",
			"extent_type=loose",
			"resolutions=%s"  % resos_s
		]
		s += "\n".join(lst)
		s += "\n\n"

	print s	
	out_path = "/etc/tilecache.cfg"	
	G.write_file(out_path, s)
	
	
"""	
	[fgx_850_ils_marker]
type=WMS
url=http://map.fgx.ch:81/mapnik/fgxwms.py?&TRANSPARENT=TRUE&
extension=png
bbox=-20037508.34,-20037508.34,20037508.34,20037508.34
srs=EPSG:3857
levels=20
metaTile=true
metaSize=2,2
metaBuffer=128
extent_type=loose
resolutions=156543.03390624999883584678,78271.51695312499941792339,39135.75847656249970896170,19567.87923828124985448085,9783.93961914062492724042,4891.96980957031246362021,2445.98490478515623181011,1222.99245239257811590505,611.49622619628905795253,305.74811309814452897626,152.87405654907226448813,76.43702827453613224407,38.21851413726806612203,19.10925706863403306102,9.55462853431701653051,4.77731426715850826525,2.38865713357925413263,1.19432856678962706631,0.59716428339481353316,0.29858214169740676658
"""	