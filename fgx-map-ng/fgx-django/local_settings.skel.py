

DEBUG = True
TEMPLATE_DEBUG = DEBUG

## Temp Directory
#TEMP_DIR = ROOT + "/_temp"

## DB at https://pg.fgx.ch:10995/

# python-yaml python-git python-memcache

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'fgx-map-ng',                      
        'USER': 'fgxmap2',                    
        'PASSWORD': 'secret',                 
        'HOST': 'localhost',                    
        'PORT': '',             
    }
}

