#!/usr/bin/python
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not remove this copyright notice.

import sys, csv, os, re
sys.path.append("/usr/local/lib/python/site-packages");

if sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "":
   print "Usage: apt-extractor.py <apt.dat> <ICAO>"
   sys.exit(0)
   
if not os.path.exists(sys.argv[1]):
	print "Sorry, file not here, and also not there. Check paths."
	print "Usage: apt-extractor.py <apt.dat> <ICAO>"
	sys.exit(0)
	

inputfile = sys.argv[1]
aptreader = open(inputfile, 'r')

datversion = "unknown"

def versionline():
	versionreader = open(inputfile, 'r')
	for versionline in versionreader.readlines():
		if versionline.startswith("810"):
			return "810"
			break
		elif versionline.startswith("850"):
			return "850"
			break

datversion = versionline()

outputfile = sys.argv[2] + "_" + datversion + ".dat"

aptwriter = open(outputfile, 'w')

searchstring = sys.argv[2]

def singleoutput():
	airportfound = 0
	for line in aptreader.readlines():
		if airportfound == 0:
			if re.search(searchstring,line):
				airportfound = 1
				print "Found airport: "+searchstring+" ... writing to file."
				aptwriter.write(line)
		else:
			if line.startswith("\n"):
				break
			aptwriter.write(line)
	aptwriter.close()

singleoutput()
	
print "Finished. Please check for '"+outputfile+"'"

