#!/usr/bin/python

from time import strftime, localtime

def publisher_example(req):
    req.content_type = 'text/html'
    time_str = strftime("%a %b %d %H:%M:%S %Y", localtime())
    message = "<h1>Hello from mod_python!</h1>"
    message += "<p>The time on this server is %s</p>" % (time_str)
    return message

