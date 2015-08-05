DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bigsurvey',
        'USER': 'root',
        'PASSWORD': '1qaz@WSX'
    }
}

DEBUG = True

ALLOWED_HOSTS = [
    'bfp-services.ltestl.com',
]

HOST = 'http://bfp-services.ltestl.com'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/itattractor/request.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
