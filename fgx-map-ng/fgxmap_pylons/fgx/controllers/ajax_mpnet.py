
import urllib2
import logging
import json

from pylons import response
from pylons.decorators import jsonify
from pylons import app_globals

from fgx.lib.base import BaseController, render

from fgx.model import meta
from fgx.model.mpnet import MpServer

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
		payload['mpservers'] = [ob.dic() for ob in obs]
		
		return payload

		
		
