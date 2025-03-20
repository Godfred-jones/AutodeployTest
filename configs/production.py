import os
from datetime import timedelta
import sentry_sdk

from base import *
from .base import env

DEBUG = False

SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["example.com"])

# MIDDLEWARE += [
#     "django.middleware.security.SecurityMiddleware",
#     "whitenoise.middleware.WhiteNoiseMiddleware",
# ]

# STATIC_ROOT = ROOT_DIR / "staticfiles"

# STATICFILES_STORAGE = (
#     "whitenoise.storage.CompressedManifestStaticFilesStorage"  # <-- Updated!
# )

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ALLOWED_ORIGINS = [
#     "https://example.com",
#     "http://localhost:8080",
#     "http://127.0.0.1:9000",
# ]





DATABASES["default"] = env.db("DATABASE_URL")  # noqa F405
DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Mimicing memcache behavior.
            # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
            "IGNORE_EXCEPTIONS": True,
        },
    }
}


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)

INSTALLED_APPS += ["storages"]  # noqa F405
GS_DEFAULT_ACL = "publicRead"

GS_BUCKET_NAME = os.getenv("GS_BUCKET_NAME")
GS_EXPIRATION = timedelta(days=7)

GS_BLOB_CHUNK_SIZE = 8 * 1024 * 1024

# 🚧 ----------------------------------- COME HERE! ----------------------------------------- 🚧 #
STATICFILES_STORAGE = "applications.utils.storages.StaticRootGoogleCloudStorage"
COLLECTFAST_STRATEGY = "collectfast.strategies.gcloud.GoogleCloudStrategy"
STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"

STATIC_URL = "/static/"
STATIC_ROOT = "static"


INSTALLED_APPS = ["collectfast"] + INSTALLED_APPS

DEFAULT_FILE_STORAGE = "applications.utils.storages.MediaRootGoogleCloudStorage"
MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"

# 🚧 ------------------------------------------------------------------------------------------🚧 #


TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]



# EMAIL
# ---------------------------------------------------------------------------------------------- #

DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL", default="project <noreply@example.com>"
)

SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX",
    default="[project]",
)
INSTALLED_APPS += ["anymail"]

EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "")
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
SENDGRID_ECHO_TO_STDOUT = True

# ANYMAIL = {
#     "SENDGRID_API_KEY": env("SENDGRID_API_KEY"),
#     "SENDGRID_GENERATE_MESSAGE_ID": env("SENDGRID_GENERATE_MESSAGE_ID"),
#     "SENDGRID_MERGE_FIELD_FORMAT": env("SENDGRID_MERGE_FIELD_FORMAT"),
#     "SENDGRID_API_URL": env("SENDGRID_API_URL", default="https://api.sendgrid.com/v3/"),
# }


# LOGGING
# -------------------------------------------------------------------------------------------- #

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
    },
}




# GOOGLE Cloud Tasks
# ---------------------------------------------------------------------------------------------- #
GOOGLE_CLOUD_TASKS_ON_GAE = env.bool("GOOGLE_CLOUD_TASKS_ON_GAE", default=True)


# SENTRY
# ---------------------------------------------------------------------------------------------- #

SENTRY_DNS = os.environ.get("SENTRY_DNS")

if SENTRY_DNS:
    sentry_sdk.init(
        dsn=SENTRY_DNS,
        enable_tracing=True,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )