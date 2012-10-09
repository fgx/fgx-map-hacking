

import commands
#from apt.debfile import DebPackage
import apt_pkg

import fgx.app_global as G

from fgx.installer import packages

class Package(object):
	
	def __init__(self):
		
		self.ptype = None
		self.package = None
		self.module = None
		self.installed = None
		self.version = None

	#def __repr__(self):
	#	print "<Package: %s>" % self.package
	#	
#APT_CHECK = "dpkg-query -W -f='${Status} ${Version}' "


def check_apt(as_string=False, verbose=1):
	
	v = verbose
	
	apt_pkg.init()
	
	cache = apt_pkg.Cache()
	
	lst = []
	for p in packages.APT:
		
		ob = Package()
		ob.ptype = "apt"
		ob.package = p
		ob.installed = None
		if not p in cache:
			ob.installed = "UNKNOWN"
			
		else:
			pkg = cache[p]
			if pkg.current_ver:
				ob.installed = True
				ob.version = pkg.current_ver.ver_str

		lst.append( ob )

		
	if as_string:
		s = "Debian Packages Installed:\n"
		for l in lst:
			s += "   %s: " % l.package.rjust(20, " ")
			s += "%s  " % ( "Yes" if l.installed else "No ")
			s += "%s\n" % ( l.version if l.installed else "")
		return s
		
	return lst


def install_apt_list():
	
	lst = check_apt()
	
	for l in lst:
		print lst
	
	
	
def install_apt():
	
	print install_list()
	
	
##===========================================================

def check_py(as_string=False):
	
	lst = []
	for p in packages.PY:
		
		ob = Package()
		ob.ptype = "py"
		ob.module = p[0]
		ob.package = p[1]
		ob.installed = False
		
		try:
			module = __import__(modo)
			ob.installed = True
		except: # ImportError
			#print "error"
			pass
	
		lst.append(ob)
	
	
	return lst