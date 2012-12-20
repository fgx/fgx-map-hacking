##@package fgx.controllers.ajax_airports
# @brief Airports, runways and other airport related controllers
#
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from sqlalchemy import or_

from fgx.lib.base import BaseController, render

from fgx.lib import helpers as h
from fgx.model import meta, Airport, Runway
from fgx.queries import airports

log = logging.getLogger(__name__)

class AjaxAirportsController(BaseController):



	@jsonify
	def airports(self):
	
		payload = {'success': True}

		apt_ident = h.v(request, "apt_ident")
		apt_name_ascii = h.v(request, "apt_name_ascii")
		
		# TODO
		#bounds = h.v(request, "bounds")
		bounds = None
		
		if apt_ident or apt_name_ascii or bounds:
			payload['airports'] = airports.airports(
											apt_ident=apt_ident, 
											apt_name_ascii=apt_name_ascii, 
											bounds=bounds)
		
		else:
			payload['error'] = "Need a ?search  or ?bounds "
			payload['aiports'] = []
			
		return payload
		
	@jsonify	
	def airports_icao(self, al=None, a2=None, a3=None, a4=None):
		
		payload = {'success': True}
		
		for i in [1,2,3,4]:
			pass
		
		
	
		return payload
		
	@jsonify
	def airport(self, apt_ident):
	
		apt_ident = apt_ident.upper()
		payload = {'success': True}
		
		
		
		payload['airport'] = airports.airport(apt_ident)
		#payload['airport'] = airports.airport(apt_ident)
		runways = meta.Sess.navdata.query(Runway
					).filter_by(apt_ident=apt_ident
					).order_by(Runway.rwy_ident).all()
		payload['runways'] = [ r.tree() for r in runways]
		
			
		return payload
		
		
		
	@jsonify
	def airport_tree(self, apt_ident):
	

		apt_ident = apt_ident.upper()
		payload = {'success': True}

		#dic = dict(apt_ident=apt_ident,
					
		
		
		payload['airport'] = airports.airport(apt_ident)
		#payload['airport']['runways'] = []
		
		#payload['airport'] = airports.airport(apt_ident)
		#payload['runways'] = airports.runways(apt_ident)
			
		return payload
		
	@jsonify
	def airport_metar(self, apt_ident):
	
		apt_ident = apt_ident.upper()
		payload = {'success': True}

		return payload
		