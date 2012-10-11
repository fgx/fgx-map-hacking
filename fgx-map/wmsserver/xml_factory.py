# (c) 2011 Yves Sablonier, Zurich, Licence: GNU GPLv2
# Do not remove this copyright notice !

# Code based on core and examples provided by Dane Springmeyer & Co.
# at the famous Mapnik2 project: http://code.google.com/p/mapnik-utils/
# Abstract: OGCServer provides a Mapnik WMS server for your data

# Create WMS Factory, load xml

from ogcserver.WMS import BaseWMSFactory

class WMSFactory(BaseWMSFactory):
  def __init__(self):
    BaseWMSFactory.__init__(self)
    self.loadXML('resources.xml')
    self.finalize()
