#!/usr/bin/env python

import os
import sys
from twisted.internet import reactor, protocol, task

host = 'mpserver01.flightgear.org'
port = 5001

class MpTelnetClient( protocol.Protocol ):

	def dataReceived( self, data ):
		print "dataReceived=", data
		## Parse lines to flight data 
		flights = []
		for line in data.split( "\n" ):
			#print line
			line = line.strip()

			if line.startswith( '#' ) or line == '':
				pass
			else:
				# we got a data line
				dic = {}
				parts = line.split( ' ' )
				#print ">>", parts, "\n"
				if parts[0].find( '@' ) != -1:
					try:
						callsign, server = parts[0].split( '@' )
						dic['callsign'] = callsign
						dic['server'] = server

						 # eg Aircraft/A340-600/Models/A340-600-Models.xml
						dic['model'] = os.path.basename( parts[10] )[0:-4]

						dic['lat'] = parts[4]
						dic['lon'] = parts[5]
						dic['altitude'] = parts[6]
						"""
						calculate heading, roll and pitch
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
						flights.append( dic )
					except:
						print "err=", sys.exc_info()[0]
						#print line
						#print parts
						#print "\n"
						#print data
						#sys.exit( 0 )


class MpTelnetClientFactory( protocol.ClientFactory ):


	def buildProtocol( self, addr ):
		print "buildProtocol", addr
		self.client = MpTelnetClient()
		return self.client

	def startedConnecting( self, connector ):
		print 'Started to connect.'

	def clientConnectionLost( self, connector, reason ):
		"""mpServer will always disconnect after sending data"""
		print 'Connection LOST. Reason:', reason

	def clientConnectionFailed( self, connector, reason ):
		"""@todo: catch error and mark server as dead.. use another"""
		print 'Connection failed. Reason:', reason


def poll_mpserver():
	#m = MpTelnetClientFactory()
	reactor.connectTCP( host, port, MpTelnetClientFactory() )

l = task.LoopingCall( poll_mpserver )
l.start( 1.0 )

## This needs to be called every second in a thread
#reactor.connectTCP( host, port, MpTelnetClientFactory() )
reactor.run()

