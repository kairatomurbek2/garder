import paypalrestsdk

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
PAYPAL_CLIENT_ID = 'AVZyLVR5fCHOkBg6DV1nnglHwOslvh6jcjE3eX1aFooPineCUITsJzcixOpqXoBxyZDO38GdocDVFl1f'
PAYPAL_CLIENT_SECRET = 'EJVZ7Zlc7SgoBTsK7lbDBPiVlFmBgxlKFv1FcEetpKIaydhw2HchpLXqsRypD6KaqM4zjQ3FwzFpg6Z5'

paypalrestsdk.configure({
    'mode': PAYPAL_MODE,
    'client_id': PAYPAL_CLIENT_ID,
    'client_secret': PAYPAL_CLIENT_SECRET,
})
