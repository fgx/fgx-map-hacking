##@package fgx.controllers.ajax_mpnet
# @brief Controllers and functions for the MultiPlayer network
#

import urllib2
import logging
import json

from pylons import response
from pylons.decorators import jsonify
from pylons import app_globals

from fgx.lib.base import BaseController, render

from fgx.model import meta
#from fgx.model.mpnet import MpServer, FlightWayPoint, BotControl, TrafficLog

log = logging.getLogger(__name__)


def get_crossfeed(plain=False):

	req = urllib2.Request(app_globals.crossfeed_data_url)
	response = urllib2.urlopen(req)
	cf_data_str = response.read()
	if plain:
		return cf_data_str
	return json.loads(cf_data_str)
	

	
	
class AjaxMpnetController(BaseController):


	@jsonify
	def flights(self):
		payload = dict(success=True,
						flights=mylib.get_flights_function())
		return payload

		
	## Return the string straight from upstream
	@jsonify
	def crossfeed(self):
		data = get_crossfeed()
		payload = dict(succes=True)
		payload.update(data)
		
		#response.headers['Content-Type'] = "text/plain"
		#payload = dict(success=True,flights=  )
		return payload

	@jsonify
	def mpstatus(self):
		payload = dict(success=True)
		obs = meta.Sess.mpnet.query(MpServer).all()
		payload['mpstatus'] = [ob.dic() for ob in obs]
		
		return payload
		
		
	@jsonify
	def bots(self):
		payload = dict(success=True)
		
		obj = meta.Sess.mpnet.query(BotControl).first()
		payload['bot_status'] = obj.dic()
		payload['bots'] = BotControl.BOTS
		
		return payload
	

			
	@jsonify
	def bot(self, bot_name, bot_action):
		
		payload = dict(success=True)
		
		running = True if bot_action == "start" else False
		
		ob = meta.Sess.mpnet.query(BotControl).first()
		
		if bot_name == "tracker":
			ob.tracker_enabled = running
			
		elif bot_name == "mpstatus":
			ob.mpstatus_enabled = running
		
		elif bot_name == "crossfeed":
			ob.crossfeed_enabled = running
		
		meta.Sess.mpnet.commit()
		
		payload['bots'] = ob.dic()
		
		return payload#
		
		