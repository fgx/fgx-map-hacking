
import socket
import threading
import time
import datetime
import telnetlib


from fgx.model import meta
from fgx.model.mpnet import MpServer, BotControl


class MpStatusThread(threading.Thread):
	

	DEBUG = False
	
	def __init__(self, config):
		threading.Thread.__init__(self)
		

	
	
	def host_name(self, server_no):
		return "mpserver%02d.flightgear.org" % server_no
	
	
	def lookup(self, server_no):
	
		"""Looks up a server"""
		domain_name = self.host_name(server_no)
		try:
			socket.setdefaulttimeout(10)
			ip_address = socket.gethostbyname(domain_name)
			#print socket.getaddrinfo(domain_name, 5000)
			if self.DEBUG:
				print "  > Found ADDR: %s = %s " % (domain_name, ip_address)
			return True, {'host': domain_name, 'no': server_no, 'ip': ip_address}
			
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
				ob = meta.Sess.mpnet.query(MpServer).get(server_no)
				if ob == None:
					ob = MpServer()
					ob.no = server_no
					ob.fqdn = self.host_name(server_no)
					ob.lag = None
					ob.last_seen = None
					meta.Sess.mpnet.add(ob)
					
				ob.ip = details['ip']
				ob.lat = details['lat']
				ob.lon = details['lon']
				ob.country = details['country']
				ob.time_zone = details['time_zone']
				
				ob.last_checked = datetime.datetime.now()
				ob.status = "unknown"
				meta.Sess.mpnet.commit()
				
				

				lag, flights = self.fetch_telnet(server_no, True)
				if lag > 0:
					ob.lag = lag
					ob.last_seen = datetime.datetime.now()
				meta.Sess.mpnet.commit()	
					
				
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


	##=====================================================
	def run(self):
		print 'T> MpStatusThread: Status thread is started'
		
		botControl = meta.Sess.mpnet.query(BotControl).get(1)
		if botControl == None:
			## This should only run on the first setup, 
			botControl = BotControl()
			botControl.mpstatus_active = True
			botControl.tracker_active = False
			meta.Sess.mpnet.add(botControl)		
			meta.Sess.mpnet.commit()
		
		time.sleep(1)
				
		while True:
			
			botControl = meta.Sess.mpnet.query(BotControl).get(1)
			print "\t MpStatusThread: Status ", botControl.mpstatus_enabled
			if botControl.mpstatus_enabled:
								
				self.lookup_all()
				print "\t\t MSPTATUS done"
				botControl.mpstatus_last = datetime.datetime.utcnow()
				meta.Sess.mpnet.commit()
			
			
			#print "\t: Sleep. zzzzzzzzzzzzz a while"
			time.sleep(300) 
	
	
	
## TODO ping check
# http://blog.boa.nu/2012/10/python-threading-example-creating-pingerpy.html


	
