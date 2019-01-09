import urllib.parse as urlparse

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
    'authentication': 'http://localhost:8000',
    'base': 'http://localhost:8000',
    'booth': 'http://localhost:8000',
    'census': 'http://localhost:8000',
    'mixnet': 'http://localhost:8000',
    'postproc': 'http://localhost:8000',
    'store': 'http://localhost:8000',
    'visualizer': 'http://localhost:8000',
    'voting': 'http://localhost:8000',
}

BASEURL = 'http://localhost:8000'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'decide',
#         'PASSWORD': 'decide',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }

url = urlparse.urlparse('postgres://mgvbzsuwamkstu:b0295daff88b2758623026d0b121906d8ab6b0ee28e120b334a42284d8ef69f4@ec2-54-75-245-94.eu-west-1.compute.amazonaws.com:5432/d5q0v8pfqn73ec')
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

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


# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256

REDIS_URL = 'redis://h:p8fea4a319c13b9f1fd16e2257831fda77af130a2a81ab7ac0f4f88aa254d7e9f@ec2-63-32-230-12.eu-west-1.compute.amazonaws.com:12399'
