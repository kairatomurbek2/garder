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


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v-4893dcgs2!)^dz&#&fc^!05f%wk$r!nqru4@%feq+)841l(*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

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
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

MEDIA_URL = '/uploads/'

EXCEL_FILES_DIR = os.path.join(MEDIA_ROOT, 'excel_files')

PWS_LOGOS_DIR = os.path.join(MEDIA_ROOT, 'pws_logos')

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

EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = 587

EMAIL_USE_TLS = True

PYTHON_EXECUTABLE = os.path.join(os.path.dirname(BASE_DIR), 'virtualenv', 'bin', 'python')

MANAGE_PY = os.path.join(BASE_DIR, 'manage.py')

STUB_FILES_DIR = os.path.join(BASE_DIR, 'stub-files')

PAYPAL_MODE = 'sandbox'
PAYPAL_CLIENT_ID = 'ARuglQBjPQQo6bUYpukNqLmFgPxQlg7Vb4zt0l0Gl6CAnX67uJGYYlMF_E5RDCKHTvOIyk3oRhFWkzuS'
PAYPAL_CLIENT_SECRET = 'EHUCx5wjMgFkQzqkhsWUtfG6-pzlvS72kaGafHmPu2-hfGE6ubLmS_yW9s0E_Hpq1YyNOGMFa4LPHA3G'

# without trailing slash
# required for PayPal to provide absolute return URL
HOST = 'http://127.0.0.1:8000'

DELETE_UNPAID_TESTS_AFTER_DAYS = 90

try:
    from settings_local import *
except ImportError:
    pass

paypalrestsdk.configure({
    'mode': PAYPAL_MODE,
    'client_id': PAYPAL_CLIENT_ID,
    'client_secret': PAYPAL_CLIENT_SECRET,
})