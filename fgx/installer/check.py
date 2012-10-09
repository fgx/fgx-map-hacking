

import commands
#from apt.debfile import DebPackage
import apt_pkg

import fgx.app_global as G

from fgx.installer import packages

APT_CHECK = "dpkg-query -W -f='${Status} ${Version}' "




def check_apt(as_string=True):
	
	apt_pkg.init()
	
	cache = apt_pkg.Cache()
	
	
	#print "-------------------------------"
	#print "Checking APT-Packages check_apt()"
	"""
	acquire = apt_pkg.Acquire()
	slist = apt_pkg.SourceList()
	print slist.read_main_list()
	for item in acquire.items:
		print item.desc_uri
	return
	"""
	lst = []
	for p in sorted(packages.APT):
		print "\nChecking: %s" % p
		#print  p
		
		#pkg = DebPackage(filename=p)
		
		if not p in cache:
			print "OOPS=", p
			
		else:
		
			pkg = cache[p]
			#print "  > pkg=", pkg
			#print dir(pkg)
			print "ver=", pkg.current_ver, "state=", pkg.current_state
			if 1 == 1: # or pkg.is_installed:
				print "installed=", #pkg.installed
			else:
				print "NOT ISNTALLED"
				#print pkg.name
		
		"""
		code, status = commands.getstatusoutput(APT_CHECK + p)
		print "res=",code, status
		
		installed = False
		if code == 256:
			pass
		
		elif code == 0:
			if status.startswith("install ok"):
				parts = status.split()
				installed = parts[-1]
			
		else:
			print "UNHANDLED"
		#print res[0], res[1]
		#print type(res[0])
		lst.append( [p, installed] )
		"""
	return lst