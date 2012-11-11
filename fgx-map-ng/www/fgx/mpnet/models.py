

from django.db import models


##=================================================================
## MpServer
##=================================================================
class MpServer(models.Model):
	
	class Meta:
		
		db_table = "mp_servers"
		get_latest_by = "last_checked"
		#order_with_respect_to = "aero"
		verbose_name = "MpServer"
		verbose_name_plural = "MpServers"

	MP_STATUS_CHOICES = (
		('unknown', 'Unknown'),
		('up', 'Up'),
		('down', 'Down')
	)
	no = models.AutoField(primary_key=True)
	subdomain = models.CharField(max_length=100, db_index=True) 
	fqdn = models.CharField(max_length=100, db_index=True, unique=True) 
	ip = models.IPAddressField( db_index=True)
	last_checked = models.DateTimeField(db_index=True, null=True)
	last_seen = models.DateTimeField(db_index=True, null=True)
	country = models.CharField(max_length=100, null=True)
	lag = models.IntegerField(null=True)
	status = models.CharField(max_length=20, choices=MP_STATUS_CHOICES, default="unknown")

	def __unicode__(self):
		return self.fqdn
		
		
	def dic(self):
		return { 'no': self.no,
				'fqdn': self.fqdn,
				'ip': self.ip,
				'country': self.country,
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
class MpBotInfo(models.Model):
	class Meta:
		db_table = "mp_bot_info"
		verbose_name = "MpBotInfo"
		verbose_name_plural = "MpBotInfo"
	
	id = models.AutoField(primary_key=True)
	
	last_dns_start = models.DateTimeField(null=True)
	last_dns_end = models.DateTimeField(null=True)
	
	last_check_start = models.DateTimeField(null=True)
	last_check_end = models.DateTimeField(null=True)
	
	
	