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
    'authentication': 'localhost:8000',
    'base': 'localhost:8000',
    'booth': 'localhost:8000',
    'census': 'localhost:8000',
    'mixnet': 'localhost:8000',
    'postproc': 'localhost:8000',
    'store': 'localhost:8000',
    'visualizer': 'localhost:8000',
    'voting': 'localhost:8000',
}

BASEURL = 'localhost:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'decide',
        'PASSWORD': 'decide',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256

REDIS_URL = 'redis://h:p8fea4a319c13b9f1fd16e2257831fda77af130a2a81ab7ac0f4f88aa254d7e9f@ec2-63-32-230-12.eu-west-1.compute.amazonaws.com:12399'
