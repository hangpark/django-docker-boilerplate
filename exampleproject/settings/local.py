from exampleproject.settings.base import *

DEBUG = True

ALLOWED_HOSTS = [u'localhost']


# Databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
