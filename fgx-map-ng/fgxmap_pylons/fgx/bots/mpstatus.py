
import socket
import threading
import time
import datetime
import telnetlib


import pygeoip

from fgx.model import meta
from fgx.model.multiplayer import MpServer, MpBotInfo


#print config

"""
{'city': '', 'region_name': '', 'area_code': 0, 'time_zone': 'Europe/Paris', 'dma_code': 0, 'metro_code': '', 'country_code3': 'FRA', 'latitude': 46.0, 'postal_code': '', 'longitude': 2.0, 'country_code': 'FR', 'country_name': 'France'}
"""


class MpStatusThread(threading.Thread):
	
	#def zulu():
	#	return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%Sz")
	DEBUG = True
	
	def __init__(self, config):
		threading.Thread.__init__(self)
		self.geoCity = pygeoip.GeoIP(config['temp_dir'] + '/maxmind/GeoLiteCity.dat', pygeoip.MEMORY_CACHE)

	
	
	def host_name(self, server_no):
		return "mpserver%02d.flightgear.org" % server_no
	
	
	def lookup(self, server_no):
	
		"""Looks up a server"""
		domain_name = self.host_name(server_no)
		try:
			socket.setdefaulttimeout(10)
			ip_address = socket.gethostbyname(domain_name)
			geo_data = self.geoCity.record_by_addr(ip_address)
			#print socket.getaddrinfo(domain_name, 5000)
			if self.DEBUG:
				print "  > Found ADDR: %s = %s " % (domain_name, ip_address)
			return True, {'host': domain_name, 'no': server_no, 'ip': ip_address,
							'lat': geo_data['latitude'] if geo_data else None,
							'lon': geo_data['longitude'] if geo_data else None,
							'country': geo_data['country_name'] if geo_data else None,
							'time_zone': geo_data['time_zone'] if geo_data else None
						}
			
		except socket.gaierror, e:
			if self.DEBUG:
				print "  > Error ADDR: %s = %s " % (domain_name, e)
			return False, e




	def lookup_all(self):
		
		"""Looks up all servers in range 1 to MAX_NAME_SERVER"""
		results = {}
		for server_no in range(1, 20 + 1):
			ok, details = self.lookup(server_no)
			#print ok, domain, details
			if ok:
				#results[details['host']] = details 
				ob = meta.Session.query(MpServer).get(server_no)
				if ob == None:
					ob = MpServer()
					ob.no = server_no
					ob.fqdn = self.host_name(server_no)
					ob.lag = None
					ob.last_seen = None
					meta.Session.add(ob)
					
				ob.ip = details['ip']
				ob.lat = details['lat']
				ob.lon = details['lon']
				ob.country = details['country']
				ob.time_zone = details['time_zone']
				
				ob.last_checked = datetime.datetime.now()
				ob.status = "unknown"
				meta.Session.commit()
				
				lag, flights = self.fetch_telnet(server_no, True)
				if lag > 0:
					ob.lag = lag
					ob.last_seen = datetime.datetime.now()
				meta.Session.commit()	
					
				
		return results


	def fetch_telnet(self, no, ping_mode):
	
		host_name = self.host_name(no)
		try:
			start = datetime.datetime.now()
			
			conn = telnetlib.Telnet(host_name, 5001, 5)
			data = conn.read_all()
			conn.close()
			
			delta = datetime.datetime.now() - start 
			lag = (delta.seconds * 1000) + (delta.microseconds / 1000)
			#print  "diff=", delta.seconds, delta.microseconds, ms
			
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
				flights = []
				
				for line_raw in lines:
					line = line_raw.strip()
					
					if line.startswith('#') or line == '':
						pass
					else:
						# we got a data line
						parts = line.split(' ')
						callsign, server = parts[0].split('@')
						dic = {}
						dic['callsign'] = callsign
						dic['server'] = server
						dic['model'] = os.path.basename(parts[10])[0:-4]
						dic['lat'] = parts[4]
						dic['lon'] = parts[5]
						dic['altitude'] = parts[6]
						
						ob = simgear.euler_get(float(parts[4]), float(parts[5]), # lat lon
												float(parts[7]), # ox
												float(parts[8]), # oy
												float(parts[9])  # oz
												)
						#print ob
						dic['roll'] = ob.roll
						dic['pitch'] = ob.pitch
						dic['heading'] = ob.heading
						flights.append(dic)
				return lag, flights
					
			
		except 	socket.error as err:
			#print " telnet err=", address, err
			return None, None



	def run(self):
		print 'T> MpStatusThread: Status thread is started'
		
		botInfo = meta.Session.query(MpBotInfo).get(1)
		if botInfo == None:
			## This should only run on the first setup, 
			botInfo = MpBotInfo()
			meta.Session.add(botInfo)
			
		
		meta.Session.commit()
		
		time.sleep(2)
				
		while True:
			
			print "\t MpStatusThread, awake then.. "
			
			botInfo.last_dns_start = datetime.datetime.now()
			meta.Session.commit()
			
			self.lookup_all()
			
			botInfo.last_dns_end = datetime.datetime.now()
			meta.Session.commit()
			
			
			
			print "\t: Sleep. zzzzzzzzzzzzz a while"
			time.sleep(300) 
	
	
	
## TODO ping check
# http://blog.boa.nu/2012/10/python-threading-example-creating-pingerpy.html


	
