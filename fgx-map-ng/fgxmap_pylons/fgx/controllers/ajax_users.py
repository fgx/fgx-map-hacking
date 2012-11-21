
import logging

from pylons import response, request
from pylons.decorators import jsonify
from pylons import app_globals

from fgx.lib.base import BaseController, render

from fgx.model import meta
from fgx.model.secure import User, UserLog


log = logging.getLogger(__name__)

class AjaxUsersController(BaseController):

	@jsonify
	def users(self):
		payload = dict(success=True)
		
		payload['users'] = [u.dic() for u in meta.Sess.secure.query(User).all()]
		
		return payload
		
		
	@jsonify
	def user(self, user_id):
		payload = dict(success=True)
		
		user_id = int(user_id)
	
		
		if request.method == "POST":
				
			if user_id == 0:
				
				ob = User()
				meta.Session.secure.add(ob)
				
			else:
				ob = meta.Session.secure.query(User).get(user_id)
				
			
				
			
		
		
		return payload
	
		
		
