
import sys
import os
from optparse import OptionParser
import urllib2




## Handle Command Args
usage = "usage: %prog "
parser = OptionParser(usage=usage)

parser.add_option("-s", 
					action="store_true", dest="simple", default=False,
					help="Use simple json parser"
                  )
                  
(opts, args) = parser.parse_args()

if opts.simple:
	import simplejson as json
else:
	import json

                  
URL = "http://cf.fgx.ch/data"

def fetch_data():
	req = urllib2.Request(URL)
	response = urllib2.urlopen(req)
	cf_data_str = response.read()
	#return json.loads(cf_data_str)
	return cf_data_str
	
#string = '{"success": true, "source":"cf-client", "last_updated": "2012-11-21 14:57:24", "flights": []}'
#string += '{callsign: "VAPID", lat: "44.405500", lon: "-72.613754", alt_ft: "3000", model: "737-300", server: "217.78.131.44", spd_kts: "223", heading: "345"}]}'
	
string =  fetch_data()
print "---------------------- string --------------------------------"
print string
print "----------------------- json   ------------------------------"
print json.loads(string)

print json.loads(string).keys()
