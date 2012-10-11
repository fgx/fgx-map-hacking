

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'aptdat2',                      # Or path to database file if using sqlite3.
        'USER': 'mash',                      # Not used with sqlite3.
        'PASSWORD': 'mash',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

## ??? said pete
GEOS_LIBRARY_PATH = '/usr/lib/libgeos_c.so.1'

