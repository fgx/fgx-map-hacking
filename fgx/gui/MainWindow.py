# -*- coding: utf-8 -*-
"""
@author: Peter Morgan 

"""

import sys
from PyQt4 import QtGui, QtCore

import fgx.app_global as G
from fgx.projects import projects

from BrowserWidget import BrowserWidget
from projects import ProjectWidget
from maps import LayersWidget

class FGxMainWindow( QtGui.QMainWindow ):

	TITLE = "FGx Dev"
	VER = 0.1

	def __init__( self, parent=None ):
		QtGui.QMainWindow.__init__( self )

		QtGui.QApplication.setStyle( QtGui.QStyleFactory.create( 'Cleanlooks' ) )

		## Stylesheet
		#styleSheetString = open('style/geolab_style.txt').read()
		#print "Stylesheet",  styleSheetString
		#app.setStyleSheet( styleSheetString )

		QtGui.QApplication.setOrganizationName( "FGx" )
		QtGui.QApplication.setOrganizationDomain( "fgx.ch" )
		QtGui.QApplication.setApplicationName( "FGx.dev" )
		QtGui.QApplication.setApplicationVersion( "0.0-alpha" )
		

		# Main Window
		self.setWindowTitle( '%s : %s ' % ( self.TITLE, self.VER ) )
		self.setWindowIcon( QtGui.QIcon( '../images/fav/favicon.png' ) )

		
		self.move(100, 100)
		self.setMinimumWidth(600)
		self.setMinimumHeight(600)
		
		##====================================================================
		##==== Menus ====
		self.menuFile = self.menuBar().addMenu( "System" )
		#self.actionLogin = self.menuFile.addAction( dIco.icon( dIco.Login ), "Login as different user", self.on_logout )
		# self.actionLogin.setIconVisibleInMenu( True )

		#self.menuFile.addSeparator()

		#actUp = self.menuFile.addAction( "Upgrade", self.on_upgrade )

		#self.menuFile.addSeparator()

		self.actionQuit = self.menuFile.addAction( "Quit", self.on_quit )
		self.actionQuit.setIconVisibleInMenu( True )
		
		
		##====================================================================
		##== Toolbar ==
		self.topToolBar = QtGui.QToolBar(self)
		self.topToolBar.setAllowedAreas(QtCore.Qt.TopToolBarArea)
		self.addToolBar(self.topToolBar)
	
	
		self.topToolBar.addAction("Make Docs", self.on_make_docs)
	
	
		##======================================
		## Left Dock
		#dockLayers = QtGui.QDockWidget( "Map Layers", self)
		#dockLayers.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
			
		#self.layersWidget = LayersWidget()
		#dockLayers.setWidget(layersWidget)
		
	
		#self.addDockWidget( QtCore.Qt.LeftDockWidgetArea, dockLayers)
		#layersWidget.init()
	
	
		##======================================
		## Right Doc widget
		# @todo: move this to ProjectwWidget
		proj_list = projects.projects_list()		
		for p in proj_list:
			
			dock = QtGui.QDockWidget( p['project'], self)
			dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
			
			projWidget = ProjectWidget()
			dock.setWidget(projWidget)
			projWidget.set_project(p)
			
			self.addDockWidget( QtCore.Qt.RightDockWidgetArea, dock)
			#print p
		
		
		
		##====================================================================
		##== Central TabWidget ==
		self.tabsWidget = QtGui.QTabWidget(self)
		self.setCentralWidget( self.tabsWidget )
		
		self.layersWidget = LayersWidget()
		self.tabsWidget.addTab( self.layersWidget, "Map Layers" ) 
		
		links = []
		links.append( ["Local static map", "file://%s/www_static/index.html" % G.PROJECT_ROOT] )
		links.append( ["Dev Docs", "file://%s/dev-docs/html/index.html" % G.PROJECT_ROOT] )
		links.append( ["map.fgx.ch", "http://map.fgx.ch/"] )
		links.append( ["Project", "http://fgx.ch/projects/fgx-map"] )
			
		## @todo Move to config
		for link in links:
			browser = BrowserWidget(self, page=link[1])
			#print link
			self.tabsWidget.addTab( browser, link[0] ) 
		
		self.layersWidget.init()
		
	## Quit App
	## @todo: Quit sys.exit() style or Qt,Application.quit() (geogff?)
	def on_quit( self ):
		sys.exit(0)
		
		return
		## TODO Use quit app in qt ??
		ret = QtGui.QMessageBox.warning( self, self.TITLE, "Sure you want to Quit ?", QtGui.QMessageBox.No | QtGui.QMessageBox.Yes )
		if ret == QtGui.QMessageBox.Yes:
			#G.settings.save_window( "Window", self )
			sys.exit( 0 )

			
	def on_make_docs(self):
		
		print "make docs"
		