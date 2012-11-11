#!/usr/bin/python
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#

import psycopg2, yaml, yaml.constructor


# getting a ordered dict for yaml, you will  need ordereddict backport
# for python < 2.7
#
# ............................................................................
# The yaml ordered dict code is adapted from code gisted by Eric Naeseth, 2011


try:
    # included in standard lib from Python 2.7
    from collections import OrderedDict
except ImportError:
    # try importing the backported drop-in replacement
    # it's available on PyPI
    from ordereddict import OrderedDict

class OrderedDictYAMLLoader(yaml.Loader):
    """
A YAML loader that loads mappings into ordered dictionaries.
"""

    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)

        self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(None, None,
                'expected a mapping node, but found %s' % node.id, node.start_mark)

        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError, exc:
                raise yaml.constructor.ConstructorError('while constructing a mapping',
                    node.start_mark, 'found unacceptable key (%s)' % exc, key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping
		
# ............................................................................

conf = open('database.yaml')
confMap = yaml.load(conf)
conf.close()

fields = open('airport.yaml')
airportMap = yaml.load(fields, OrderedDictYAMLLoader)
fields.close()

sqlstring = "CREATE TABLE airport ("

for i in airportMap.keys():
	if airportMap[i]['size'] == None:
		sqlstring += airportMap[i]['field'] + " " + airportMap[i]['type'] + ","# \\\n"
	else:
		sqlstring += airportMap[i]['field'] + " " + airportMap[i]['type'] + "(" + str(airportMap[i]['size']) + ")" + ","# \\\n"
	
sqlstring = sqlstring + ");"
exe = sqlstring.replace(",);",");")

print sqlstring

connectstring = "dbname=" + confMap['database'] + " user=" + confMap['user'] + " password=" + confMap['password']

conn = psycopg2.connect(connectstring)
cur = conn.cursor()
			
cur.execute("DROP TABLE IF EXISTS airport;")

cur.execute(exe)

conn.commit()
cur.close()
conn.close()

print "--- CREATED TABLE: AIRPORT ---"










