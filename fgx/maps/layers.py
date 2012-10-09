## 
# @file: layers.py
# @author: Peter Morgan 
# -*- coding: utf-8 -*-

import yaml

from fgx import app_global as G 


## Return the projects.yaml in text format
# @return string with yaml contents
def layers_raw():
	s = G.read_file("/config/layers.yaml")
	return s

## Return a list of projects from the config
# @return dict of data
def layers_dict():
	dic = yaml.load( projects_raw() )
	return dic

## Return a list of projects from the config
# @return list of data
def layers_list():
	projects_dic = projects_dict()
	lst = []
	for d in projects_dic:
		dic = projects_dic[d]
		#dic['project'] = d
		lst.append(dic)
	return lst


