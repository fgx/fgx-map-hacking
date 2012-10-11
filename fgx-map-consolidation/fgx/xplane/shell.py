#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Grabs the html from http://data.x-plane.com/update/data/


and then find the files for 850 series
AptNav******XP861.zip when ****** is YYYYMM date eg 200808

sort in ascending date order, ie earliest to latest
and then write to temp/zips.txt

"""
import sys
import os
import datetime
import yaml
import zipfile
import urllib2

from bs4 import BeautifulSoup
#from BeautifulSoup import BeautifulSoup
import operator

from fgx.shell_config import TEMP_DIR

XPLANE_URL = 'http://data.x-plane.com/update/data/'


##==========================================================================
## Zip file meta object
class AptZip(object):
	
	def __init__(self):
		
		self.file_name = None
		self.url = None
		self.dated = None

		
		
##==========================================================================
## The Server Object encompasses and caches the server calls
class Server():
	
	def __init__(self):
		
		self.files = None
		
		
		
	def fetch_index(self):
		
		if self.files:
			return self.files
		
		#== Fetch the xplane downloads files index html page
		print "> Fetching xplane index from %s" % XPLANE_URL 
		response = urllib2.urlopen( XPLANE_URL )
		html = response.read()
		#print ">> Got reply"
		#print html

		##== Parse into soup
		soup = BeautifulSoup(html)
		#print ">> parsing html for entries > "
		#print soup


		## We are ony interested in files endinf with these
		V8 = "XP861.zip"
		V10 = "XP1000.zip"
			
		##== Get all the links and loop them
		all_rows =  soup.findAll("tr")
		#print len(all_rows)
		
		## Cut off apache info
		rows  = all_rows[3:-1]
		
		lst = []
		for a in rows:
			
			## Find all <td>
			tds = a.findAll("td")
			
			#= Get the filename ie the text of the <a href="">text</a>
			file_name =  tds[1].findAll("a")[0].text
			
			if file_name.startswith("AptNav"):
				if file_name.endswith(V8) or file_name.endswith(V10):
	
					file_date_str = tds[2].text.strip()
					#print "'%s'" % file_date_str, datetime.datetime.strftime(datetime.datetime.now(), "%d-%b-%Y %H:%M")
					file_date = datetime.datetime.strptime(file_date_str, "%d-%b-%Y %H:%M")
									
					lst.append( dict(file_name=file_name, dated=file_date) )

			else:
				#print "Ignore: ", file_name
				pass
			
		#print lst
		#return
		## Sort
		files_ordered_by_date = sorted(lst, key=operator.itemgetter("dated"))
			
		self.files = []
		c = 0
		for f in files_ordered_by_date:
			#print file_date
			c += 1
			#zip_file = "AptNav%sXP861.zip" % datetime.datetime.strftime(file_date, "%Y%m")
			ob = AptZip()
			ob.c = c
			ob.url = '%s%s' % ( XPLANE_URL, f['file_name'])
			ob.file_name = f['file_name']
			ob.dated = datetime.datetime.strftime(f['dated'], "%Y-%m-%d") 
			self.files.append(ob)
			
		return self.files


	def show_index(self):
		files = self.fetch_index()
		line = ("-" * 50) + "\n"
		s = "" #< got data > parsing > \n"  
		s += line
		s += "Idx " + "Zip File".ljust(25, " ") + "  Dated\n"
		s += line
		for l in files:
			s += "%s) %s %s\n" % (str(l.c).rjust(2," "), l.file_name.ljust(25, " "), l.dated)
			
		return s

	##============================================================
	def fetch_zip(self, idx=None):
		
		fileObj = self.fetch_index()[idx - 1]
		
		#print "NFO=", fileObj
		
		download_dir = TEMP_DIR + "/downloads/"
		if not os.path.exists(download_dir):
			os.mkdir(download_dir)
		
		save_target = download_dir + fileObj.file_name
		print "save_target=%s" % save_target
		## check target exists
		if os.path.exists(save_target):
			print ">> zip file already exists in '%s' " % save_target
			print ">> checking if sane: ",
			try:
				zf = zipfile.ZipFile(save_target, "r")
				#print "test", zf.testzip()
				if zf.testzip() == None:
					print "   Yes valid zip"
					print ">> Skipping"
					return
					
			except:
				print "Error - zip appears invalid "
			#zf.close()
			#return
			
		#print ">> Downloading"
		#return
		
		u = urllib2.urlopen(fileObj.url)
		
		#print save_target
		f = open(save_target, 'wb')
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		print ">> Downloading: %s Bytes: %s" % (fileObj.file_name, file_size)

		file_size_dl = 0
		block_sz = 8192
		while True:
			buffer = u.read(block_sz)
			if not buffer:
				break

			file_size_dl += len(buffer)
			f.write(buffer)
			status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
			status = status + chr(8)*(len(status)+1)
			print status,

		f.close()
		

##==========================================================================
## Function calls
## ALSO: Please listen to "funky" by dMob, a mix by peteffs ala mash from yonder year
##==========================================================================

def print_remote_list():
	serverObj = Server()
	print serverObj.show_index()

	
def do_download():
	serverObj = Server()
	print serverObj.show_index()

	x = raw_input("Enter download Idx: (enter for cancel)? ") or None
	#print "x=", x
	if x != None:
		# @todo: Chack its an int and it exists
		serverObj.fetch_zip(idx=int(x))
		
