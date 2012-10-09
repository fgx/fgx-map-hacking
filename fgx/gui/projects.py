# -*- coding: utf-8 -*-
"""
@author: Peter Morgan
"""



from PyQt4 import QtCore, QtGui


class ProjectWidget(QtGui.QWidget):
	
	
	def __init__(self):
		QtGui.QWidget.__init__(self, parent=None)
		
		mainLayout = QtGui.QVBoxLayout()
		self.setLayout(mainLayout)
		
		self.tree = QtGui.QTreeWidget()
		mainLayout.addWidget(self.tree)
		
		self.tree.setHeaderLabels(["Node", "Value"])
		
		
		
		
	def set_project(self, dic):
		
		#self.tree
		for d in dic:
			item = QtGui.QTreeWidgetItem()
			item.setText(0, d)
			item.setText(1, dic[d])
			self.tree.addTopLevelItem(item)
			
			
		
	
	