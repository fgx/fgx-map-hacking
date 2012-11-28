#!/usr/bin/env python
#
# FGx Map Project: ogcserver.py
#
#                __,.vv._,,..,. _
#           _.. :`\_'.,_       |     =-"            '-,
#          _."\=[  '    \     /             _/''._,,-''`..,  `:|     _
#  = '`---^- 'Y' 'v '`.    _,'        .'`-.,>=.>           `'' ''----,_
#  <',...       .-'']['  ./         /[[)  `                  ___, .,^
#  .-'   `,      --`| :_            ;:,''                   :o  _'
#          |       ' ,o,`          ['._ ) \                 ,'_
#          ].                    ``_!Y`'v.-               `[_/
#            \. /-^\             ,'  ----`  `.._         )|/
#              `\. `-..        .'        ``'LY  \ ,']. `''
#                 `.v,..        ` _,_     `=     -   |'' pL
#                   '   `.._        /.    /'         `\..  ...
#                   '_     /         |    , .          '"--_| `'
#                    |    ,'             / ]             .'  -'.  ,
#                    |  ,'            :_/               ]_,,.  |
#                    |,'                                     -=    ,'
#                   ,,'                                           -
#                    --
#
# (c) 2012 Yves Sablonier, Pete Morgan, Geoff McLane
# License: GPLv2 or later
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Boston, MA 02110-1301, USA.

import os
import sys
from ogcserver.wsgi import WSGIApp

import os
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(WORKING_DIR)
configpath = os.path.join(WORKING_DIR,'ogcserver.conf')

application = WSGIApp(configpath)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('127.0.0.1', 6046, application)
    print "FGx WMS Server listening on port 6046 ..."
	
    httpd.serve_forever()
