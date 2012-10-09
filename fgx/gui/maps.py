# -*- coding: utf-8 -*-
"""
@author: Peter Morgan
"""

from PyQt4 import QtCore, QtGui

from fgx.maps import layers

class LayersWidget(QtGui.QWidget):
	
	
	def __init__(self):
		QtGui.QWidget.__init__(self, parent=None)
		
		mainLayout = QtGui.QVBoxLayout()
		self.setLayout(mainLayout)
		
		self.tree = QtGui.QTreeWidget()
		mainLayout.addWidget(self.tree)
		
		self.tree.setHeaderLabels(["Node", "Value"])
		
		
		
		
	def set_layers(self, dic):
		
		#self.tree
		for d in dic:
			item = QtGui.QTreeWidgetItem()
			item.setText(0, str(d))
			item.setText(1, str(dic[d]))
			self.tree.addTopLevelItem(item)
			
			
		
	def init(self):
		
		lst = layers.layers_list()
		print lst
		