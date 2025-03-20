from .base import *

DEBUG = True

# TODO: look at this allowed_hosts
ALLOWED_HOSTS = []

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS += ["django_extensions"]


MEDIA_URL = "/media/"
