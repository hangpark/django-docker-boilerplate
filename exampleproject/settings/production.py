import pymysql

from exampleproject.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [u'localhost']


# Databases

pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'exampleproject',
        'USER': os.getenv('DB_ENV_MYSQL_USER'),
        'PASSWORD': os.getenv('DB_ENV_MYSQL_PASSWORD'),
        'HOST': os.getenv('MYSQL_HOST') or 'db',
        'PORT': '3306',
    }
}


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = '/var/www/static'

MEDIA_ROOT = '/var/www/media'
