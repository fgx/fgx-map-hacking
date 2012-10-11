

import threading
import time

from pylons import config


from geo2pylons.model import MailQ
from geo2pylons.lib.mailq.despatcher import Despatcher 


class MailQThread(threading.Thread):
	
	def run(self):
		print 'Flights: thread is running.'
		
		time.sleep(2)
		
		d = Despatcher()
		
		while True:
			
			#print "\n-----------------------------------------------------"
			#print "MailQThread: UP"
			
			d.process_all()

			#print "\t MailQThread: Sleep. zzzzzzzzzzzzz"
			time.sleep(20)
	
def start_mailq_thread():
	worker = MailQThread()
	worker.start()
