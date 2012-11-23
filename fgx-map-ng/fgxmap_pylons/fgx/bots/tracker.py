
import socket
import threading
import time
import datetime

import urllib2
import json


from fgx.model import meta
from fgx.model.mpnet import FlightWayPoint, BotControl, TrafficLog

class TrackerThread(threading.Thread):
	
	
	DEBUG = True
	
	def __init__(self, config):
		threading.Thread.__init__(self)

		self.config = config
		
	def get_crossfeed(self, plain=False):

		req = urllib2.Request(self.config['crossfeed_ajax_url'])
		response = urllib2.urlopen(req)
		cf_data_str = response.read()
		if plain:
			return cf_data_str
		return json.loads(cf_data_str)


	def run(self):
		print 'T> TrackerThread: TrackerThread thread is started'
				
		## tracker startd after 10 seconds to allow catchup
		time.sleep(5)
				
		while True:
			
			
			botControl = meta.Sess.mpnet.query(BotControl).get(1)
			print "\t Tracker: Status ", botControl.tracker_enabled
			if botControl.tracker_enabled:
						
				data = self.get_crossfeed()
				#print data
				for f in data['flights']:
					#print f
					wp = FlightWayPoint()
					wp.time = datetime.datetime.utcnow()
					wp.callsign = f['callsign']
					wp.model = f['model']
					wp.latitude = f['lat']
					wp.longitude = f['lon']
					wp.altitude = f['alt_ft']
					wp.speed = f['spd_kts']
					wp.heading = f['hdg']
					meta.Sess.mpnet.add(wp)
					
				#meta.Sess.mpnet.commit()
			
				

				oblog = TrafficLog()
				oblog.flights = len(data['flights'])
				meta.Sess.mpnet.add(oblog)
				
				botControl.tracker_last = datetime.datetime.utcnow()
				meta.Sess.mpnet.commit()	
				
				print "\t\t tracker done"

			time.sleep(10) 
	
	

	
