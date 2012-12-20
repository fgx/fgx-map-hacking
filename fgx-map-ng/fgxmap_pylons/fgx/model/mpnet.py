##@package fgx.model.mpnet 
# @brief Access to the tracker and multiplayer network
#

import datetime

from sqlalchemy import  Boolean, Integer, Float, String, Date, DateTime, Column

from fgx.model.meta import Sess, Base




class Flight(Base.mpnet):
	
	__tablename__ = "flights"

	f_pk = Column(Integer(), primary_key=True)
	fid = Column(String(24), index=True, nullable=False, unique=True)
	callsign = Column(String(16), index=True, nullable=False)
	model = Column(String(20), index=True, nullable=True)
	
	status = Column(String(20), index=True, nullable=True)
	
	#start_time = time = Column(DateTime())
	#end_time = time = Column(DateTime(), nullable=True)
	#distance = Column(Integer(), nullable=True)
	
	#max_altimeter = Column(Integer(), nullable=True)
	#max_speed = Column(Integer(), nullable=True)
	
	
class FlightWayPoint(Base.mpnet):
	
	__tablename__ = "positions"

	p_pk = Column(Integer(), primary_key=True)
	fid = Column(String(24), nullable=False, index=True)
	ts = Column(DateTime(), nullable=False, index=True)
	
	#model = Column(String(20), nullable=True)
	
	#time = Column(DateTime(timezone=False)) #ZULU?, default=datetime.datetime.now(tz=pytz.timezone('UTC'))
	
	## We dont want geometry columns ie no GIS database
	## also lat/lon is float for calculation ... asks pete ?? 
	lat= Column(String(16), nullable=False)
	lon = Column(String(16), nullable=False)
	spd_kts = Column(Integer(), nullable=True)
	alt_ft = Column(Integer(), nullable=True)
	hdg = Column(Integer(), nullable=True)
	
	
	def dic(self):
		return {
			"time": str(self.time),
			"lat": self.latitude, "lon": self.longitude,
			"alt_ft": self.altitude,
			"spd_kts": self.speed
			}

##=================================================================
## MpServer
##=================================================================
class MpServer(Base.mpnet):
	
	__tablename__ = 'mp_server'
	
	MP_STATUS_CHOICES = (
		('unknown', 'Unknown'),
		('up', 'Up'),
		('down', 'Down')
	)
	no = Column(Integer(), primary_key=True)
	subdomain = Column(String(100), index=True) 
	fqdn = Column(String(100), index=True, unique=True) 
	ip = Column(String(16), index=True)
	last_checked = Column(DateTime(), index=True, nullable=True)
	last_seen = Column(DateTime(timezone=False), index=True, nullable=True)
	country = Column(String(100), nullable=True)
	lag = Column(Integer(), nullable=True)
	status = Column(String(20))
	
	lat = Column(String(20), nullable=True)
	lon = Column(String(20), nullable=True)
	#wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)
	
	country = Column(String(50), nullable=True)
	time_zone = Column(String(50), nullable=True)

	def __unicode__(self):
		return self.fqdn
		
		
	def dic(self):
		return { 'no': self.no,
				'fqdn': self.fqdn,
				'ip': self.ip,
				'country': self.country,
				'last_checked': str(self.last_checked),
				'last_seen': str(self.last_seen) if self.last_seen else None,
				'lag': self.lag,
				'lat': self.lat,
				'lon': self.lon,
				'country': self.country,
				'time_zone': self.time_zone
		}
		
		
		
	@staticmethod
	def fqdn_from_no(server_no):
		return "mpserver%02d.flightgear.org" % server_no
	
	@staticmethod
	def subdomain_from_no(server_no):
		return "mpserver%02d" % server_no	
		
		
##=================================================================
## Bot Control and state
##=================================================================


	
## Records when the bot last did a DNS check
class BotControl(Base.mpnet):
	
	BOTS = ["mpstatus", "crossfeed", "tracker"]
	
	__tablename__ = "bot_control"

	id = Column(Integer(), primary_key=True)
	

	mpstatus_enabled = Column(Boolean(), nullable=True)
	mpstatus_last  = Column(DateTime(), nullable=True)
	
	tracker_enabled = Column(Boolean(), nullable=True)
	tracker_last  = Column(DateTime(), nullable=True)
	
	crossfeed_enabled = Column(Boolean(), nullable=True)
	crossfeed_last  = Column(DateTime(), nullable=True)
	
	def dic(self):
		return dict(
			mpstatus_enabled = self.mpstatus_enabled,
			mpstatus_last = str(self.mpstatus_last),
			
			tracker_enabled = self.tracker_enabled,
			tracker_last = str(self.tracker_last),
			
			crossfeed_enabled = self.crossfeed_enabled,
			crossfeed_last = str(self.crossfeed_last)
		)
		
		
		

