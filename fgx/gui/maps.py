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
		
		for l in lst:
			item = QtGui.QTreeWidgetItem()
			item.setText(0, str(l['layer']))
			item.setFirstColumnSpanned(True)
			self.tree.addTopLevelItem(item)
			self.tree.setFirstItemColumnSpanned(item, True)
			self.tree.setItemExpanded(item, True)
			dic = l
			del dic['layer']
			self.add_dict(item, dic)
			
			#for d in dic:
			#	sitem = QtGui.QTreeWidgetItem(item)
			#	sitem.setText(0, str(d))
			#	sitem.setText(1, str(dic[d]))
			
			
	def add_dict(self, pItem, dic):
		
		for d in dic:
			sitem = QtGui.QTreeWidgetItem(pItem)
			sitem.setText(0, str(d))
			
			if isinstance(dic[d], dict):
				kItem = self.add_dict(sitem, dic[d])
				#self.tree.setItemExpanded(sitem, True)
			else:	
				sitem.setText(1, str(dic[d]))
			
			
				