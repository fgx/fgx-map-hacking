#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Peter Morgan 
@version: 0.1
"""

import sys
from PyQt4 import QtGui, QtCore

#import main.dDev
#from main import make_splash

import MainWindow

def run_gui():
    app = QtGui.QApplication( sys.argv )


    #splashScreen = main.make_splash()

    #app.processEvents()


    window = MainWindow.FGxMainWindow()


    #splashScreen.finish( window )
    
    window.show()

    sys.exit( app.exec_() )
    


if __name__ == '__main__':

    run_gui()


