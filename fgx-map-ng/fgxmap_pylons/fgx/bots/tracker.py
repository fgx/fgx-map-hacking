
import socket
import threading
import time
import datetime

import urllib2
import json


from fgx.model import meta
from fgx.model.mpnet import FlightWayPointss

class TrackerThread(threading.Thread):
	
	
	DEBUG = True
	
	def __init__(self, config):
		threading.Thread.__init__(self)

		self.config = config
		
	def get_crossfeed(self, plain=False):

		req = urllib2.Request(self.config.crossfeed_data_url)
		response = urllib2.urlopen(req)
		cf_data_str = response.read()
		if plain:
			return cf_data_str
		return json.loads(cf_data_str)


	def run(self):
		print 'T> TrackerThread: TrackerThread thread is started'
		
		"""
		botInfo = meta.Sess.mpnet.query(MpBotInfo).get(1)
		if botInfo == None:
			## This should only run on the first setup, 
			botInfo = MpBotInfo()
			meta.Sess.mpnet.add(botInfo)
			
		
		meta.Sess.mpnet.commit()
		"""
		
		time.sleep(2)
				
		while True:
			
			print "\t TrackerThread, awake then.. "
			
			#botInfo.last_dns_start = datetime.datetime.now()
			#meta.Sess.mpnet.commit()
			
			#self.lookup_all()
			
			#botInfo.last_dns_end = datetime.datetime.now()
			#meta.Sess.mpnet.commit()
			
			
			
			print "\t: Sleep. zzzzzzzzzzzzz a while"
			time.sleep(300) 
	
	

	
