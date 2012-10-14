#!/usr/bin/env python


import sys
import os
import datetime
import telnetlib
import socket
import json

from django.core.cache import cache

import settings
#from fgx.mpnet.models import MpServer



## Represents a reply 
class MpReply(object):
	def __init__(self):	
		self.error = None
		self.address = None
		self.lag = None
		self.flights = None
	


##---------------------------------------------
## Fetch telnet data from MP Server admin port
# @todo Need to set a timeout of 5 seconds, but not work atmo
# @param address fqdn or ip of server
# @param ping_mode - True return lab, False return flights parsed
# @retval Mp Object
def fetch_telnet(address,  ping_mode):

	reply = MpReply()
	reply.address = address
	
	try:
		start = datetime.datetime.now()
		
		conn = telnetlib.Telnet()
		#conn.settimeout(5)
		conn.open(address, 5001, 5)
		data = conn.read_all()
		conn.close()
		
		delta = datetime.datetime.now() - start 
		reply.lag = (delta.seconds * 1000) + (delta.microseconds / 1000)
		#print  "diff=", delta.seconds, delta.microseconds, ms

	except 	socket.error as err:
		#print " telnet err=", address, err
		reply.error = err
		return reply
		
	lines = data.split("\n")
	
	if ping_mode: # MP Ping Mode
		tracked = "@ Not Tracked"
		if lines[2].find("tracked") != -1:
			tracked = lines[2]
			
		if lines[3].find("tracked") != -1:
			tracked = lines[3]
			
			
		pilots = "@ No Pilots"
		if lines[2].find("pilots") != -1:
			pilots = lines[2]
			
		if lines[3].find("pilots") != -1:
			pilots = lines[3]
		
		return lag, {'info': lines[0],
					'version': lines[1],
					'tracked': tracked,
					'pilots': pilots
					}
		
	else: # Flights Mode
		reply.flights = []
		
		for line_raw in lines:
			line = line_raw.strip()
			
			if line.startswith('#') or line == '':
				pass
			else:
				# we got a data line
				#print line
				if line.startswith("* Bad Client *"):
					print "BAD_CLIENT=", line
				else:	
					parts = line.split(' ')
					callsign, server = parts[0].split('@')
					dic = {}
					dic['callsign'] = callsign
					dic['server'] = server
					dic['model'] = os.path.basename(parts[10])[0:-4]
					dic['lat'] = parts[4]
					dic['lon'] = parts[5]
					dic['altitude'] = parts[6]
					
					"""
					ob = simgear.euler_get(	float(parts[4]), float(parts[5]), # lat lon
											float(parts[7]), # ox
											float(parts[8]), # oy
											float(parts[9])  # oz
											)
					
					#print ob
					dic['roll'] = ob.roll
					dic['pitch'] = ob.pitch
					dic['heading'] = ob.heading
					"""
					reply.flights.append(dic)
		return reply
				
		




def ping_run():
	
	#fp = open(conf.DNS_FILE, "r")
	
	#dns = json.load(fp)
	#fp.close()
	#print dns
	mpservers = MpServer.objects.all()
	
	results = []
	for mp in MpServer.objects.all():
		ok, details = fetch_telnet(mp.ip, False)
		print "TELNET=", mp.no, ok,  details
		
		mpOb = MpServer.objects.get(pk=mp.no)
		
		#return 
		if ok:
			results.append( details )
	return results


## Updates the memcache with flightdata
# Keys are "flights" and "last_update"
def update_cache():
	
	reply = fetch_telnet(settings.FGX_MP_SERVER, False)
	dt = str(datetime.datetime.now())
	if not reply.error:
		cache.set("flights", reply.flights)
		cache.set("last_update", dt )
		print "updated cache", dt
	else:
		print "Cache update fail", dt
	
	
	
