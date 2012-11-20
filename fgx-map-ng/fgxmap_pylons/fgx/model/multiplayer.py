

from sqlalchemy import  Integer, String, Date, DateTime, Column


from fgx.model.meta import Sess, Base


##=================================================================
## MpServer
##=================================================================
class MpServer(Base):
	
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
## Bot Info
##=================================================================

## Records when the bot last did a DNS check
class MpBotInfo(Base):
	
	__tablename__ = "mp_bot_info"

	id = Column(Integer(), primary_key=True)
	
	last_dns_start = Column(DateTime())
	last_dns_end = Column(DateTime())
	
	last_check_start = Column(DateTime())
	last_check_end = Column(DateTime())

	