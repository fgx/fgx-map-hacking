#!/usr/bin/env python
#
# FGx Map Project: wms.py
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

import sys
sys.path.append('/home/map/fgx-map/fgx-map-ng/wmsserver')

from ogcserver.cgiserver import Handler
from jon import fcgi

class OGCServerHandler(Handler):
    configpath = '/home/map/fgx-map/fgx-map-ng/wmsserver/ogcserver.conf'

fcgi.Server({fcgi.FCGI_RESPONDER: OGCServerHandler}).run()
