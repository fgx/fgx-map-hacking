# -*- coding: utf-8 -*-
"""
@author: Peter Morgan 

"""

import sys
from PyQt4 import QtGui, QtCore

from fgx import config
from BrowserWidget import BrowserWidget



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
        
        
        
        
        
        
        ##====================================================================
        ##== TabWidget ==
        self.tabsWidget = QtGui.QTabWidget(self)
        self.setCentralWidget( self.tabsWidget )
        
        links = []
        links.append( ["Local static map", "file://%s/www_static/index.html" % config.PROJECT_ROOT] )
        links.append( ["Dev Docs", "file://%s/dev-docs/html/index.html" % config.PROJECT_ROOT] )
        links.append( ["map.fgx.ch", "http://map.fgx.ch/"] )
        links.append( ["Project", "http://fgx.ch/projects/fgx-map"] )
        
        
        
        for link in links:
            browser = BrowserWidget(self, page=link[1])
            print link
            self.tabsWidget.addTab( browser, link[0] ) 
        
        
    def on_quit( self ):
        sys.exit(0)
        
        return
        ## TODO Use quit app in qt ??
        ret = QtGui.QMessageBox.warning( self, self.TITLE, "Sure you want to Quit ?", QtGui.QMessageBox.No | QtGui.QMessageBox.Yes )
        if ret == QtGui.QMessageBox.Yes:
            #G.settings.save_window( "Window", self )
            sys.exit( 0 )
