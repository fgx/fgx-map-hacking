
import logging

from pylons import response
from pylons.decorators import jsonify
from pylons import app_globals

from fgx.lib.base import BaseController, render

from fgx.model import meta
from fgx.model.mpnet import MpServer

log = logging.getLogger(__name__)

class AjaxUsersController(BaseController):

	@jsonify
	def users(self):
		payload = dict(success=True)
		
		return payload
		
		
	@jsonify
	def user(self, user_pk):
		payload = dict(success=True)
		
		user_pk = int(user_pk)
	
		
		if request.method == "POST":
				
			if user_pk == 0:
				
				ob = User()
				meta.Session.secure.add(ob)
				
			else:
				ob = meta.Session.secure.query(User).get(user_pk)
				
			
				
			
		
		
		return payload
	
		
		
