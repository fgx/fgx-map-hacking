
import urllib2
import logging
#import simplejson as json

from pylons import response
from pylons.decorators import jsonify
from pylons import app_globals

from fgx.lib.base import BaseController, render

log = logging.getLogger(__name__)


def get_crossfeed():

	req = urllib2.Request(app_globals.crossfeed_data_url)
	response = urllib2.urlopen(req)
	cf_data_str = response.read()
	#return json.loads(cf_data_str)
	return cf_data_str

	
	
class AjaxMpnetController(BaseController):


	@jsonify
	def flights(self):
		payload = dict(success=True,
						flights=mylib.get_flights_function())
		return payload

		
	## Return the string straight from upstream
	def crossfeed(self):
		data_str = get_crossfeed()
		response.headers['Content-Type'] = "text/plain"
		#payload = dict(success=True,flights=  )
		return data_str
