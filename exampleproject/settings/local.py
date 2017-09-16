from kaistrule.settings.base import *

DEBUG = True

ALLOWED_HOSTS = [u'localhost']


# Databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files

LOCAL_DIR = os.path.join(BASE_DIR, 'local')

STATIC_ROOT = os.path.join(LOCAL_DIR, 'static')

MEDIA_ROOT = os.path.join(LOCAL_DIR, 'media')
