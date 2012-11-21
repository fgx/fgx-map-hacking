
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
	
	
string =  fetch_data()
print "---------------------- string --------------------------------"
print string
print "----------------------- json   ------------------------------"
print json.loads(string)

