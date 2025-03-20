from .base import *
from .base import env

DEBUG = True

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="EX7K7Wxf4AgYoFBeSXuyzDia2B4v5WCwgumhoOSvMwFeoEvkNi2EbzawqqHaOFRF",
)

ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]


# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}


DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
# if env("USE_DOCKER", "no") == "yes":
#     import socket

#     hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
#     INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

INSTALLED_APPS += ["django_extensions"]


# Your stuff...
# ------------------------------------------------------------------------------
GS_BUCKET_NAME = env.str("GS_BUCKET_NAME", "")
