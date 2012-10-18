
import os
import json
import yaml
from string import Template


from fgx.xmap import layers
from fgx import helpers as h
from fgx import settings
    
## Write out the layers.js file
# @param ln If true creates a symlink to www_static/js/layers.js
def write_js(ln=True):
	
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
		s += "  {visibility: %s}\n" % ("true" if d['visibility'] else "false")
		s += "));\n"
		js_str += s
		print s
	
		
	out_path = "/etc/config.js"	
	h.write_file(out_path, js_str)
		
	if ln:
		ln_path = settings.ROOT + "/www_static/js/config.js"
		print "exits", os.path.exists( ln_path ), ln_path
		if os.path.exists( ln_path ):
			print "  > removed link: " + ln_path
			os.remove(ln_path)
		print "  > created sym link: " + ln_path	
		os.symlink(settings.ROOT + out_path, ln_path)
		
		ln_path = settings.ROOT + "/fgx/static/js/config.js"
		if os.path.exists( ln_path ):
			print "  > removed link: " + ln_path
			os.remove(ln_path)
		print "  > created sym link: " + ln_path
		os.symlink(settings.ROOT + out_path, ln_path)
	
## Writes out nginx config
# @ todo by pete
def write_nginx(ln=False):
	
	s = "server: "
	
	out_path = "/etc/nginx.conf"	
	h.write_file(out_path, s)
	
	
## Writes out \b local_config.yaml	
def write_local_config(dic):
	
	s = yaml.dump(dic)
	h.write_file("/local_config.yaml", s)
	
	
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
	h.write_file(out_path, s)
	

def print_install_info():
	print "==============================="
	print "ROOT = %s" % settings.ROOT
	
	print "Install Checklist: >>"
	
	## @TODO: check this lot is installed
	
	dic = h.read_yaml("/config/install.yaml")
	for ki in dic:
		d = dic[ki]
		print " > %s " % ki
		#print dic[d]
		print "   > %s " % d['info']
		print "   > Packages: "
		for p in d['packages']:
			# TODO echeck it exists etc
			print "      > %s "  % p
		
		
		
	
	
	