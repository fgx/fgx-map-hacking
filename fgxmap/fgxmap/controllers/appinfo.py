import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from fgxmap.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AppinfoController(BaseController):


	@jsonify
	def sys_info(self):

		payload = dict(foo="bar")

		return payload
