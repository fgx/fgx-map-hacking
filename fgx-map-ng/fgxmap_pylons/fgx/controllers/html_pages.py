##@package fgx.controllers.html_pages
# @brief Html pages and other non ajax stuff
#
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from fgx.lib.base import BaseController, render
from fgx.lib import helpers as h

from fgx.config import style

log = logging.getLogger(__name__)

class HtmlPagesController(BaseController):

	
	def index(self, page=None):
		
		c.page = page if page else "map-ext"	
		
		return render("%s.html" % c.page)
	
	"""
	def maptest(self):
		return render("map-test.html")
		
	def database(self):
		return render("database.html")
		
		
	def admin_users(self):
		return render("admin_users.html")
		
	"""	
	
	## Serves the css for the Ext4 icons, these are defined in config.style
	# 
	# This appears at the url  <b>/dynamic.{fgx_js_version}.css</b>
	# @see lib.app_globals.Globals.fgx_js_version
	# @see config.style.get_icons_css()
	def dynamic_icons_css(self):
		txt = style.get_icons_css()
		response.headers['Content-Type'] = "text/css";
		return txt
		
	"""	
	def fg_server_xml_cgi(self):
		
		s = '<?xml version="1.0" encoding="UTF-8" ?>'
		s += '<fg_server pilot_cnt="%s">' % len(flights)
		for f in flights:
			
		<marker callsign="jvmr" server_ip="LOCAL" model="747-400" lat="25.433817" lng="-64.117113" alt="20418.908292" heading="334.428619384766" pitch="-0.287139564752579" roll="-0.0248698983341455" />
    <m
		
		return "FOoooooooooooooooooo"
	"""
	
	""" Am trying to future prrof with various flavours of mobile eg /m/ext or /m/jsmobile etc """
	def mobile(self, page=None):
		
		mobile_template = "mobile.html"
		if page:
			mobile_template = "mobile.%s.html"
		
		return render(mobile_template)
		
		