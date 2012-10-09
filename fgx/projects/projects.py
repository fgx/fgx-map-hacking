## @package fgx
# @file: projects.py
# @author: Peter Morgan 
# -*- coding: utf-8 -*-

import yaml

from fgx import app_global as G 


## Return the projects.yaml in text format
def projects_raw():
	

## Return a list of projects from the config
def projects_dict():
	
	dic = yaml.load( G.read_file("/config/projects.yaml") )
	
	return dic

	