## 
# @file: layers.py
# @author: Peter Morgan 
# -*- coding: utf-8 -*-

import yaml
import json

from fgx import app_global as G 


## Return the layers.yaml in text format
# @return string with yaml contents
def layers_raw():
	s = G.read_file("/config/layers.yaml")
	return s

## Return a list of layers from the config
# @return dict of data
def layers_dict():
	dic = yaml.load( layers_raw() )
	return dic

## Return a list of layers from the config
# @return list of data
def layers_list():
	layers_dic = layers_dict()
	lst = []
	for d in layers_dic:
		dic = layers_dic[d]
		dic['layer'] = d
		lst.append(dic)
	return lst


def resolutions_raw():
	s = G.read_file("/config/resolutions.yaml")
	return s
	
def resolutions():
	dic = yaml.load( resolutions_raw() )
	return dic['resolutions']