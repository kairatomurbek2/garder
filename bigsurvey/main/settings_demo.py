DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bigsurvey',
        'USER': 'root',
        'PASSWORD': '1qaz@WSX'
    }
}

EMAIL_HOST_USER = "bss.bpsbr.com@gmail.com"

EMAIL_HOST_PASSWORD = "febAt62Aruwethe"

DEFAULT_FROM_EMAIL = "bss.bpsbr.com@gmail.com"

REPLY_TO_EMAIL = "bss.bpsbr.com@gmail.com"

RETURN_PATH_EMAIL = "bss.bpsbr.com@gmail.com"

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
