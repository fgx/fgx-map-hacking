## @package fgx
# @file: projects.py
# @author: Peter Morgan 
# -*- coding: utf-8 -*-

import yaml

from fgx import app_global as G 


## Return the projects.yaml in text format
# @return string with yaml contents
def projects_raw():
	s = G.read_file("/config/projects.yaml")
	return s

## Return a list of projects from the config
# @return dict of data
def projects_dict():
	dic = yaml.load( projects_raw() )
	return dic

## Return a list of projects from the config
# @return list of data
def projects_list():
	projects_dic = projects_dict()
	lst = []
	for d in projects_dic:
		dic = projects_dic[d]
		dic['project'] = d
		lst.append(dic)
	return lst


