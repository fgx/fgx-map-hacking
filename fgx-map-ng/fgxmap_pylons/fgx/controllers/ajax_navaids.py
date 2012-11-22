import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from sqlalchemy import or_

from fgx.lib.base import BaseController, render
from fgx.lib import helpers as h

from fgx.model import meta
from fgx.model.data import NavAid
from fgx.queries import navaids

log = logging.getLogger(__name__)



class AjaxNavaidsController(BaseController):

	@jsonify
	def navaids(self):
		payload = {'success': True}
		
		search = h.v(request, "search")
		nav_type = h.v(request, "nav_type")
		
		if search:
			payload['navaids'] = navaids.search(search=search, nav_type=nav_type)
		
		else:
			payload['rows'] = []
			payload['error'] = "Need a ?search="
		
		return payload
		
		
		
	@jsonify
	def fix(self, ident=None):
		
		payload = {'success': True}
		if ident:
			
			payload['LOOK'] = "TODO"
			
		else:
			q = request.params['q'].upper()
			
			obs = meta.Session.query(Fix).filter(Fix.ident.contains(q)).limit(100).all()
			
			payload['rows'] = [ob.dic() for ob in obs]
		
		
		return payload
		

	@jsonify
	def ndb(self, ident=None):
		
		payload = {'success': True}
		if ident:
			
			payload['LOOK'] = "TODO"
			
		else:
			q = request.params['q'].upper()
			
			obs = meta.Session.query(Ndb).filter(or_(Ndb.ident.contains(q), Ndb.name.contains(q))).limit(100).all()
			
			payload['rows'] = [ob.dic() for ob in obs]
		
		
		return payload	

		
	@jsonify
	def vor(self, ident=None):
		
		payload = {'success': True}
		if ident:
			
			payload['LOOK'] = "TODO"
			
		else:
			q = request.params['q'].upper()
			
			obs = meta.Session.query(Vor).filter(or_(Vor.ident.contains(q), Vor.name.contains(q))).limit(100).all()
			
			payload['rows'] = [ob.dic() for ob in obs]
		
		
		return payload	
		
	@jsonify	
	def process_flightplan(self):
		payload = {'success': True}
		
		raw = h.v(request, "raw_text")
		
		waypoints = raw.split()
		
		flight_plan = []
		idx = 0
		uid = 0
		for w in waypoints:
			##obs = meta.Sess.data.query(NavAid).filter_by(ident=w).all()
			points = navaids.search(ident=w)
			idx += 1
			if len(points) == 0:
				flight_plan.append( {"wp": w, "idx": idx, "ident": w, "uid": uid, 'nav_type': None, 'lat': None, 'lon': None, 'freq': None} )
				uid += 1
			else:
				for p  in points:
					dic = {"wp": w, "idx": idx, "uid": uid}
					dic.update(p)
					flight_plan.append(dic)
					uid += 1
			
		
		
		payload['waypoints'] = waypoints
		payload['flight_plan'] = flight_plan
	
	
		return payload	
	
	