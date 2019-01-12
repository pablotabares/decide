import os

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}


ALLOWED_HOSTS = ['*']

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

BASEURL = 'https://decide-ortosia.herokuapp.com'

APIS = {
    'authentication': 'https://decide-ortosia.herokuapp.com',
    'base': 'https://decide-ortosia.herokuapp.com',
    'booth': 'https://decide-ortosia.herokuapp.com',
    'census': 'https://decide-ortosia.herokuapp.com',
    'mixnet': 'https://decide-ortosia.herokuapp.com',
    'postproc': 'https://decide-ortosia.herokuapp.com',
    'store': 'https://decide-ortosia.herokuapp.com',
    'visualizer': 'https://decide-ortosia.herokuapp.com',
    'voting': 'https://decide-ortosia.herokuapp.com',
}

STATIC_ROOT = os.path.dirname(os.path.abspath(__file__))+'/static'
MEDIA_ROOT = os.path.dirname(os.path.abspath(__file__))+'/static/media'
