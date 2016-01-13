from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': "/media/ramdisk/db.sqlite3",
    }
}

EMAIL_HOST_USER = "bss.bpsbr.com@gmail.com"

EMAIL_HOST_PASSWORD = "febAt62Aruwethe"

DEFAULT_FROM_EMAIL = "bss.bpsbr.com@gmail.com"

REPLY_TO_EMAIL = "bss.bpsbr.com@gmail.com"

RETURN_PATH_EMAIL = "bss.bpsbr.com@gmail.com"
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

FIREFOX_PROFILE_DIR = os.path.join(os.path.dirname(BASE_DIR), 'firefox-profile')

REINITIALIZE_DATABASE = True
