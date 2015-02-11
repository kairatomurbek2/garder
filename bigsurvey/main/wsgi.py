"""
WSGI config for bigsurvey project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
import site

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

site.addsitedir(BASE_DIR+'/../virtualenv/lib/python2.7/site-packages')
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
