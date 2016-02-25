import paypalrestsdk

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
PAYPAL_MODE = 'live'
PAYPAL_CLIENT_ID = 'AVZyLVR5fCHOkBg6DV1nnglHwOslvh6jcjE3eX1aFooPineCUITsJzcixOpqXoBxyZDO38GdocDVFl1f'
PAYPAL_CLIENT_SECRET = 'EJVZ7Zlc7SgoBTsK7lbDBPiVlFmBgxlKFv1FcEetpKIaydhw2HchpLXqsRypD6KaqM4zjQ3FwzFpg6Z5'

paypalrestsdk.configure({
    'mode': PAYPAL_MODE,
    'client_id': PAYPAL_CLIENT_ID,
    'client_secret': PAYPAL_CLIENT_SECRET,
})


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
