"""
Django settings for bigsurvey project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import paypalrestsdk

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/
TWENTY_MBYTES = 20971520
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v-4893dcgs2!)^dz&#&fc^!05f%wk$r!nqru4@%feq+)841l(*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'webapp', 'templates'),
    os.path.join(BASE_DIR, 'auditlog', 'templates'),
)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webapp',
    'accounts',
    'lettuce.django',
    'webapp_features',
    'django_extensions',
    'widget_tweaks',
    'pagination',
    'ckeditor',
    'reversion',
    'reversion_compare',
    'auditlog',
    'captcha',
    'ajax_select',
)

SESSION_COOKIE_AGE = 900
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'webapp.middlewares.demo_trial_watch_dog.DemoTrialWatchDog',
    'webapp.middlewares.renew_session_on_activity.RenewSessionOnActivity',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "webapp.processor.use_captcha"
)

ROOT_URLCONF = 'main.urls'

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bigsurvey',
        'USER': 'root',
        'PASSWORD': '1qaz@WSX'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Central'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Email configuration
EMAIL_HOST = 'smtp.office365.com'
EMAIL_HOST_USER = 'garderpassword@bssbr.net'
EMAIL_HOST_PASSWORD = '$oftware1'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "garderpassword@bssbr.net"
REPLY_TO_EMAIL = "bss@bpsbr.com"
RETURN_PATH_EMAIL = "bss@bpsbr.com"
PWS_REGISTATION_FROM_EMAIL = "garder@bssbr.net"

# captcha configuration
RECAPTCHA_PUBLIC_KEY = '6LfQkBYTAAAAAOqc6TFVt7PoLEr44_mV4zN_-B_s'
RECAPTCHA_PRIVATE_KEY = '6LfQkBYTAAAAAObzDbh8tOCaoO7OKiZFZPOVdjCb'
NOCAPTCHA = False
CAPTCHA_AJAX = True
USE_CAPTHCA = True

# Demo trial configuration
DEMO_TRIAL_DAYS = 30
PERIOD_DEMO_TRIAL = 10

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

WEBAPP_FIXTURES_BASE = os.path.join(BASE_DIR, 'webapp', 'fixtures')

SAMPLE_DATA_JSON = os.path.join(WEBAPP_FIXTURES_BASE, 'sample_data_for_pws_registration.json')

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA = os.path.join(BASE_DIR, 'uploads/media')

MEDIA_URL = '/uploads/'

EXCEL_FILES_DIR_NAME = 'excel_files'

EXCEL_FILES_DIR = os.path.join(MEDIA_ROOT, EXCEL_FILES_DIR_NAME)

EXCEL_EXPORT_DIR = os.path.join(MEDIA_ROOT, 'excel_export')

EXPORT_BASE_URL = MEDIA_URL + 'excel_export/'

PWS_LOGOS_DIR = os.path.join(MEDIA_ROOT, 'pws_logos')
TAC_PDF_DIR = os.path.join(MEDIA_ROOT, 'media')

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Hello',
        'toolbar_Hello': [
            ['Format', 'Font', 'FontSize'],
            ['Bold', 'Italic', 'Underline', 'Strike', '-', 'TextColor', 'BGColor', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Image', 'Table', '-', 'Link', 'Unlink'],
            ['Undo', 'Redo'],
            ['Source']
        ],
        'allowedContent': True,
        'width': '100%',
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"

PYTHON_EXECUTABLE = os.path.join(os.path.dirname(BASE_DIR), 'virtualenv', 'bin', 'python')

MANAGE_PY = os.path.join(BASE_DIR, 'manage.py')

STUB_FILES_DIR = os.path.join(BASE_DIR, 'stub-files')

PAYPAL_MODE = 'sandbox'
PAYPAL_CLIENT_ID = 'AV2p3Oa0Jf2O-MUdOPjm70z1pAm293geK0yy6oli4ZLkd3MEaef_glGLTi7tv2jtuEQZ8M-KENeBILZw'
PAYPAL_CLIENT_SECRET = 'EE-ar9o_saSWsZzGgtuaH0sDP4XLvqYtb5Yd9KgFysRtNjR18oYc1o7J99xgrSy8Y3ztz52KICcagMHL'

# without trailing slash
# required for PayPal to provide absolute return URL
HOST = 'http://127.0.0.1:8000'

DELETE_UNPAID_TESTS_AFTER_DAYS = 2

DELETE_OLD_XLS_FILES_AFTER_DAYS = 10

ADMINS = (
    ('GARDER', 'bss.bpsbr.com@gmail.com'),
)
MANAGERS = ADMINS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': TWENTY_MBYTES,
            'filename': 'debug_log.txt',
        },

        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }

    },
    'loggers': {
        'django.request': {
            'handlers': ['file','mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

try:
    from settings_local import *
except ImportError:
    pass

paypalrestsdk.configure({
    'mode': PAYPAL_MODE,
    'client_id': PAYPAL_CLIENT_ID,
    'client_secret': PAYPAL_CLIENT_SECRET,
})


#backup settings
BACKUPS_DIR = os.path.join(os.path.dirname(BASE_DIR), 'backups')
BACKUPS_DIR_PWS = '/home/garder/backup/'

CREATE_BACKUP_SCRIPT = os.path.join(os.path.dirname(BASE_DIR), 'create_backup.sh')

RESTORE_BACKUP_SCRIPT = os.path.join(os.path.dirname(BASE_DIR), 'restore_backup.sh')
