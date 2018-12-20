import psycopg2
import urllib.parse as urlparse
import os

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

ALLOWED_HOSTS = ["*"]

# Modules in use, commented modules that you won't use
MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]

APIS = {
    'authentication': os.environ['APP_URL']+':80',
    'base': os.environ['APP_URL']+':80',
    'booth': os.environ['APP_URL']+':80',
    'census': os.environ['APP_URL']+':80',
    'mixnet': os.environ['APP_URL']+':80',
    'postproc': os.environ['APP_URL']+':80',
    'store': os.environ['APP_URL']+':80',
    'visualizer': os.environ['APP_URL']+':80',
    'voting': os.environ['APP_URL']+':80',
}

BASEURL = os.environ['APP_URL']+':80'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': dbname,
        'USER': user,
	    'PASSWORD': password,
        'HOST': host,
        'PORT': port,
    }
}

STATIC_ROOT = os.path.dirname(os.path.abspath(__file__))+'/static'

STATIC_URL = '/static/'

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256
