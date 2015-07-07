from settings import *

MIGRATION_MODULES = {"webapp": "webapp.migrations_not_used_in_tests"}  # in order to make tests not to run migrations

# SQLite
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db', 'unittest.db.sqlite3'),
#     }
# }

# MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bigsurvey',
        'USER': 'root',
        'PASSWORD': ''
    }
}

EMAIL_HOST_USER = "bss.bpsbr.com@gmail.com"

EMAIL_HOST_PASSWORD = "febAt62Aruwethe"

DEFAULT_FROM_EMAIL = "bss.bpsbr.com@gmail.com"

REPLY_TO_EMAIL = "bss.bpsbr.com@gmail.com"

RETURN_PATH_EMAIL = "bss.bpsbr.com@gmail.com"
