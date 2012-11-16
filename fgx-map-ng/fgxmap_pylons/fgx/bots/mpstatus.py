
import threading
import time

from pylons import config

from fgx.model import meta, MpServer, MpBotInfo

#from geo2pylons.model import MailQ
#from geo2pylons.lib.mailq.despatcher import Despatcher 


class MpStatusThread(threading.Thread):
	
	def run(self):
		print 'T> MpStatusThread: Status thread is started'
		
		botInfo = meta.Session.query(MpBotInfo).get(1)
		if botInfo == None:
			## This should only run on the first setup, 
			botInfo = MpBotInfo()
			meta.Session.add(botInfo)
			
		botInfo
		meta.Session.commit()
		
		time.sleep(2)
		
		#d = Despatcher()
		
		while True:
			
			#print "\n-----------------------------------------------------"
			#print "MailQThread: UP"
			
			#d.process_all()

			print "\t MpStatusThread, awake then.. "
			time.sleep(2)
			print "\t.. Todo lookup the dns servers.... low priority"
			time.sleep(10)
			print "\t: Sleep. zzzzzzzzzzzzz a while"
			time.sleep(60)
	
def start_mpstatus_thread():
	worker = MpStatusThread()
	worker.start()
	
	