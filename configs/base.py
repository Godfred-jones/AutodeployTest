import os
from pathlib import Path

import environ

ROOT_DIR = Path(__file__).resolve().parent.parent

APPS_DIR = ROOT_DIR / "applications"

env = environ.Env()

# envfile = str(ROOT_DIR / ".env")
# envpath = Path(envfile)

# if envpath.exists():
#     env.read_env(envfile)
# else:
#     pass

# ------------------

# READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
# if READ_DOT_ENV_FILE:
#     # OS environment variables take precedence over variables from .env
#     env.read_env(str(ROOT_DIR / ".env"))

# ------------------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

EXTRA_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_spectacular",
    # "drf_yasg",
]

LOCAL_APPS = [
    "applications.common.apps.CommonConfig",
    "applications.users.apps.UsersConfig",
]

INSTALLED_APPS = DJANGO_APPS + EXTRA_APPS + LOCAL_APPS


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_USER_MODEL = "users.User"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

MIDDLEWARE += [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "configs.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # TODO: Don't hard code templates dir
        "DIRS": [str(APPS_DIR / "templates")],
        # "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "applications.utils.context_processors.settings_context",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

# Passowrds
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    # https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

WSGI_APPLICATION = "configs.wsgi.application"

SITE_ID = 1

ADMIN_URL = "admin/"
ADMINS = []
MANAGERS = ADMINS

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Fixtures - https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# Internationalization - https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
USE_L10N = True
# LOCALE_PATHS = [str(ROOT_DIR / "locale")]

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
CORS_URLS_REGEX = r"^/api/.*$"

# LOGGING - https://docs.djangoproject.com/en/dev/ref/settings/#logging
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}


# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="project <noreply@example.com>",
    # https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
)

EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
    # https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
)
EMAIL_TIMEOUT = 5


# SECURITY
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# CORS_ORIGIN_ALLOW_ALL = True

# DATABASES
# ---------------------------------------------------------------------------------
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"  # https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field


# STATIC FILES - https://docs.djangoproject.com/en/5.0/howto/static-files/
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = str(APPS_DIR / "media")
MEDIA_URL = "/media/"


# REST FRAMEWORK
# ---------------------------------------------------------------------------------
REST_FRAMEWORK = {"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"}


# DJOSER SETTINGS
# ------------------------------------------------------------------------------
DJOSER = {
    "HIDE_USERS": False,
    "SERIALIZERS": {
        "user": "applications.users.serializers.UserSerializer",
    },
}


# SWAGGER SETTINGS
# -----------------------------------------------------------------------------
TOKEN_DESCRIPTION = """
Once you have a valid access token you
need to add it as a HTTP header to every HTTP request you send to the Spikizi API.
`Authorization: Token <key>` \n
When the user [logs out](#operation/auth_logout_create), this API token is expired, and
a new one created the next time the user logs in. `\n
A token is also generated at [registration](#operation/auth_registration_create) .\n
Usage format: `Token <key>`\n
"""

API_BASE_URL = env.str("API_BASE_URL", "http://localhost:8000/api")

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Token": {
            "description": TOKEN_DESCRIPTION,
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
        }
    },
    "DEFAULT_API_URL": API_BASE_URL,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "API Documentation",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}
