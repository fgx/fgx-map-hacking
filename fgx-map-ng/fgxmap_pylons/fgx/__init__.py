##@package fgx
# @brief The pylons wsgi web service
#
# This Web Server Gateway Interface (wsgi) application is currently
# using the good olde Pylons framework.
# http://docs.pylonsproject.org/projects/pylons-webframework/en/latest/
# 
# ============
# Intro
# ============
# This section details how to get the webserver up and running.
# At FGx we are running behind nginx/paster on the server and
# also for dev at the moment so same enviroment.
#
# However there are a lot of parts to make up the mix and include
# - static content eg javascript libraries, stock images
# 
#
# ---------------
# JS Libraies, icons etc are loaded from http://static.fgx.ch
# This is a checkout of fgx-static repos which contains the 
# content. 
# Note: content is served directly by nginx and is CACHED FOREVER.
#      so please be careful.
#
#