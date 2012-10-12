

DEBUG = True
TEMPLATE_DEBUG = DEBUG



DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'aptdat3',                      
        'USER': 'mash',                    
        'PASSWORD': 'mash',                 
        'HOST': 'localhost',                    
        'PORT': '',             
    }
}

## ??? said pete
#GEOS_LIBRARY_PATH = '/usr/local/lib/libgeos.so'
#G#EOS_LIBRARY_PATH = '/usr/lib/libgeos_c.so.1' 
#GEOS_LIBRARY_PATH = '/usr/local/lib/libgeos_c.so'


#GDAL_LIBRARY_PATH = '/home/sue/local/lib/libgdal.so'
