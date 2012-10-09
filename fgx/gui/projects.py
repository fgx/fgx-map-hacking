# -*- coding: utf-8 -*-
"""
@author: Peter Morgan
"""



from PyQt4 import QtCore, QtGui


class ProjectWidget(QtGui.QWidget):
	
	
	def __init__(self):
		QtGui.QWidget.__init__(self )
		
		mainLayout = QtGui.QVBoxLayout()
		self.setLayout(mainLayout)
		
		self.tree = QtGui.QTreeWidget()
		mainLayout.addWidget(self.tree)
		
		self.tree.setHeaderLabels(["Node", "Value"])
		
		
		
		
		
	
	