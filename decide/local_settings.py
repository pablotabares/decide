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
    'authentication': 'https://ortosia-auth.herokuapp.com/',
    'base': 'https://ortosia-auth.herokuapp.com/',
    'booth': 'https://ortosia-auth.herokuapp.com/',
    'census': 'https://ortosia-auth.herokuapp.com/',
    'mixnet': 'https://ortosia-auth.herokuapp.com/',
    'postproc': 'https://ortosia-auth.herokuapp.com/',
    'store': 'https://ortosia-auth.herokuapp.com/',
    'visualizer': 'https://ortosia-auth.herokuapp.com/',
    'voting': 'https://ortosia-auth.herokuapp.com/',
}

BASEURL = 'https://ortosia-auth.herokuapp.com/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'decide',
        'USER': 'decide',
        'PASSWORD': 'decide',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256
