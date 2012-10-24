

import os
import sys

## Absolute path to the GIT_ROOT
GIT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


## Absolute path to the project root ie abve dganjo in currently in fgx-map-ng
PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

## Absolute path to the django app , currently in fgx/
APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))

TEMP_DIR = None
DATA_DIR = None

DEBUG = False
TEMPLATE_DEBUG = DEBUG

FGX_STATIC_URL = "http://static.fgx.ch"

FGX_SRID = 3857

#FGX_MP_SERVER = "mpserver14.flightgear.org"
FGX_MP_SERVER = "217.150.241.103"


# Global configuration
BROWSER_SECRET_KEY = 'Ianreakkboredwitheveryonegettingexistedaboutprofilightsimandtheirfailuretodomainateamarketwithfreesotwarepackeagedupandamciriousaboutthatfactwitharevenuevscontribandallkidsonxboxwithaccountsinmindsecret'

# Flask-Cache settings
CACHE_TYPE = 'memcached'
CACHE_MEMCACHED_SERVERS = ['127.0.0.1:11211']

# When behind a load balancer, set CANONICAL_NAME to the value contained in
# Host headers (e.g. 'www.example.org')
CANONICAL_NAME = '127.0.0.1'

# When behind a load balancer, set CANONICAL_PORT to the value contained in
# Host headers (normally it will be '80' in production)
CANONICAL_PORT = '8866'

DATABASE_URI_FMT = 'postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{dbname}'
DB_HOST = '127.0.0.1'
DB_NAME = 'skeleton'
# Setup a password database. Generate a random pass via:
# import M2Crypto
# M2Crypto.m2.rand_bytes(24).encode('base64').rstrip()
DB_PASS = ''
DB_PORT = '5432'
DB_SCHEMA = 'skeleton_schema'
DB_ADMIN = 'skeleton_dba'
DB_USER = 'skeleton_www'
DEBUG = True
DEBUG_TOOLBAR = False
LISTEN_HOST = '127.0.0.1'
PASSWORD_HASH = ''
SECRET_KEY = 'is_anything_secret_anymore?'
SESSION_BYTES = 25
SESSION_COOKIE_NAME = 'fgx_is_cool_session'

SSL_CERT_FILENAME = ''
SSL_PRIVATE_KEY_FILENAME = ''
TESTING = False
USE_SSL = False

# Logs SQL queries to stderr
SQLALCHEMY_ECHO = False

# If users want to pass specific werkzeug options
WERKZEUG_OPTS = {'host': LISTEN_HOST, 'port' : 8866}


#######################################################
# Import user-provided values
try:
	from local_settings import *
except ImportError:
	print "Fatal Error: `local_settings.py` is missing"
	sys.exit(0)

## idiot checks
if TEMP_DIR == None:
	print "Fatal Error: No  `TEMP_DIR` in `local_settings.py`"
	sys.exit(0)

if DATA_DIR == None:
	print "Fatal Error: No  DATA_DIR in `local_settings.py`"
	sys.exit(0)


# Derived values
SQLALCHEMY_DATABASE_URI = DATABASE_URI_FMT.format(**
	{   'username': DB_USER,
		'password': DB_PASS,
		'hostname': DB_HOST,
		'port':     DB_PORT,
		'dbname':   DB_NAME,
		'schema':   DB_SCHEMA,
	})

# Explicitly specify what's a local request
scheme = 'https' if USE_SSL else 'http'
LOCAL_REQUEST = '%s://%s:%s/' % (scheme, CANONICAL_NAME, CANONICAL_PORT)


