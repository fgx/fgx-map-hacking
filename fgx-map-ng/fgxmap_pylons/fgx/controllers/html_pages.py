import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from fgx.lib.base import BaseController, render

log = logging.getLogger(__name__)

class HtmlPagesController(BaseController):

	
	def index(self):
		return render("map-ext.html")
	
	def maptest(self):
		return render("map-test.html")
		
	def database(self):
		return render("database.html")
		
		
	def admin_users(self):
		return render("admin_users.html")
		
		
