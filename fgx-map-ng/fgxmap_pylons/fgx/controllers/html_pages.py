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
		c.ext_theme = None
		ext_theme_to_set = h.v(request, 'ext_theme')
		if ext_theme_to_set:
			response.set_cookie( "ext_theme" , ext_theme_to_set, max_age=180*24*3600 )
			c.ext_theme = ext_theme_to_set
		else:
			c.ext_theme = request.cookies.get("ext_theme")
		if c.ext_theme == None:
			c.ext_theme = "xtheme-gray.css"
		
		
		return render("%s.html" % c.page)
	
	"""
	def maptest(self):
		return render("map-test.html")
		
	def database(self):
		return render("database.html")
		
		
	def admin_users(self):
		return render("admin_users.html")
		
	"""	
	def dynamic_icons_css(self):
		txt = style.get_icons_css()
		response.headers['Content-Type'] = "text/css";
		return txt
		
