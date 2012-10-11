

import os
APP_ROOT = os.path.abspath( os.path.join(os.path.dirname(__file__), "../"))


DEBUG = True
TEMPLATE_DEBUG = DEBUG


## Zulu time
TIME_ZONE = 'UTC'




TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(APP_ROOT, "templates")
)

STATIC_ROOT = APP_ROOT

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	os.path.join(APP_ROOT, 'static'),
)



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'aptdat',                      # Or path to database file if using sqlite3.
        'USER': 'mash',                      # Not used with sqlite3.
        'PASSWORD': 'mash',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

