#!/usr/bin/env python

## This script looks up the dns entry for mp servers
## Saves the disovered server to mpservers.json

import sys
import os


import threading
import time
import socket
import json


from django.utils import timezone as dtz 
from django.contrib.gis.geoip import GeoIP

from fgx.mpnet.models import MpServer, MpBotInfo
from fgx.mpnet import mp_telnet



class DnsLookupThread (threading.Thread):
	
	def __init__(self):
		
		self.max_dns_no = 0
		
		threading.Thread.__init__(self)
		
	def get_bot_info(self):
		"""Return the singular mpBitInfo record used for persistance, or creates one first time"""
		##TODO make this into a try catch with get(pk=1) maybe .. I dont f care
		botInfos = MpBotInfo.objects.filter(id=1)
		if len(botInfos) == 0:
			botInfo = MpBotInfo()
			botInfo.save()
			return botInfo
		return botInfos[0]
		
		
	def run(self):
		
		botInfo = self.get_bot_info()
		
		while True:
			
			print "DNS_THREAD: Starting DNS Lookup" 
			botInfo.last_dns_start = dtz.now()
			botInfo.save()
			
			self.lookup_all()
			
			botInfo.last_dns_end = dtz.now()
			botInfo.save()
			
			print "DNS_THREAD: End DNS: sleeping"
			time.sleep(30)

		
	def lookup_all(self):

		"""Looks up all servers in range 1 to MAX_NAME_SERVER"""
		
		## we always get to the max se this should be 10 above the last set of servers kinda.. said pete
		#self.max_dns_no = 
		lookup_max = 30 #self.max_dns_no + 10  ## HEH
		results = {}
		for server_no in range(1, lookup_max):
			ok, details = self.lookup(server_no)
			#print ok, domain, details
			if ok:
				results[details['fqdn']] =  details 
		return results
		
		
	def lookup( self, server_no ):
		
		"""Looks up a server"""
		fulldomain = MpServer.fqdn_from_no(server_no)
		subdomain = MpServer.subdomain_from_no(server_no)
		try:
			socket.setdefaulttimeout(10)
			ip_address = socket.gethostbyname(fulldomain)
			# print "  > Found ADDR: %s = %s " % (fulldomain, ip_address)
				
			results = MpServer.objects.filter(fqdn=fulldomain)
			if len(results) == 0:
				MP = MpServer(	no=server_no, fqdn=fulldomain, subdomain=subdomain, ip=ip_address )
			else:
				MP = results[0]
			
			#TODO some IP adddress change detectio and triggger
			MP.ip = ip_address
			
			g = GeoIP()
			MP.country =  g.country(ip_address)['country_name']
			
			MP.save()
				
			return True, {'fqdn': MP.fqdn, 'no': MP.no, 'ip': MP.ip}
			
		except socket.gaierror, e:
			if conf.DEBUG:
				print "  > Error ADDR: %s = %s " % (fulldomain, e)
			return False, e

	
	
	