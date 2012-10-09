# -*- coding: utf-8 -*-
"""
@author: Peter Morgan 

"""

import sys
from PyQt4 import QtGui, QtCore




class FGxMainWindow( QtGui.QMainWindow ):

    TITLE = "FGx Dev"
    

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
        
        
        self.move(100, 100)
        self.setMinimumWidth(600)
        self.setMinimumHeight(600)
        
        

