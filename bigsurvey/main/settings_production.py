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

PYTHON_PATH = '/home/bigsurvey/projects/bigsurvey/virtualenv/bin/python'

PAYPAL_MODE = 'live'
PAYPAL_CLIENT_ID = 'AcNRSqnM9S50OODwjRagn7M1DE-ggvYBuXUKAcV2plScA5_I0HFp-zGPz3jApqXZtmEdRC2ZVAuZi4RP'
PAYPAL_CLIENT_SECRET = 'EH8uorRlRwHAPP4lWRKPpULVGc3RxZGp_t7WwAWP1JWf4kkcn9AoAt-YA8175iagc7rynFYBp_t2ldEG'

paypalrestsdk.configure({
    'mode': PAYPAL_MODE,
    'client_id': PAYPAL_CLIENT_ID,
    'client_secret': PAYPAL_CLIENT_SECRET,
})
