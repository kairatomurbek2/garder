DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bigsurvey',
        'USER': 'bigsurvey_user',
        'PASSWORD': 'B5S51fZtjWu8Nwa'
    }
}

DEBUG = False

ALLOWED_HOSTS = [
    'bss.bpsbr.com',
]

HOST = 'http://bss.bpsbr.com'

PAYPAL_MODE = 'live'
PAYPAL_CLIENT_ID = 'AVZyLVR5fCHOkBg6DV1nngIHwOslvh6jcjE3eX1aFooPineCUITsJzcixOpqXoBxyZDO38GdocDVFI1f'
PAYPAL_CLIENT_SECRET = 'EJVZ7Zlc7SgoBTsK7lbDBPiVIFmBgxIKFv1FcEetpKlaydhw2HchpLXqsRypD6KaqM4zjQ3FwzFpg6Z5'