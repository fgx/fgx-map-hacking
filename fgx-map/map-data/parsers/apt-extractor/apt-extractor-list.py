#!/usr/bin/python
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not remove this copyright notice.

import sys, csv, os, re
sys.path.append("/usr/local/lib/python/site-packages");

if sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "":
   print "Usage: python apt-extractor-list.py <apt.dat> <ICAO-list.txt>"
   sys.exit(0)
   
if not os.path.exists(sys.argv[1]):
	print "Sorry, file not here, and also not there. Check paths."
	print "Usage: python apt-extractor-list.py <apt.dat> <ICAO-list.txt>"
	sys.exit(0)
	
	
inputfile = sys.argv[1]
inputlistfile = sys.argv[2]

dir = "extracted"

if not os.path.exists(dir):
    os.makedirs(dir)

datversion = "unknown"

def versionline():
	versionreader = open(inputfile, 'r')
	for versionline in versionreader.readlines():
		
		if versionline.startswith("810"):
			datversion = "810"
			return datversion
			#break
		
		if versionline.startswith("850"):
			datversion = "850"
			return datversion
			#break
			
datversion = versionline()

def singleoutput(searchstring):
	airportfound = 0
	
	aptreader = open(inputfile, 'r')
	outputfile = "extracted/"+searchstring + "_" + datversion + ".dat"
	aptwriter = open(outputfile, 'w')
	
	for line in aptreader.readlines():
		if airportfound == 0:
			if re.search(searchstring,line):
				airportfound = 1
				print "Processing: "+searchstring+" ... writing to file."
				aptwriter.write(line)
		else:
			if line.startswith("\n") or line.startswith("\r\n"):
				airportfound = 0
				break
			aptwriter.write(line)
	aptwriter.close()
	print "Created '"+outputfile+"'"


def dothejob():
	
	aptlistreader = open(inputlistfile, 'r')
	for listline in aptlistreader.readlines():
		listline2 = listline.replace("\n","")
		print listline2
		string = listline2
		print "Looking for ... "+string
		singleoutput(string)
		
dothejob()
	

	


