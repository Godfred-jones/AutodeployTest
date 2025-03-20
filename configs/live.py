import sentry_sdk
from base import *

DEBUG = False

ALLOWED_HOSTS = []

MIDDLEWARE += [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"  # <-- Updated!
)

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ALLOWED_ORIGINS = [
#     "https://example.com",
#     "http://localhost:8080",
#     "http://127.0.0.1:9000",
# ]


SENTRY_DNS = os.environ.get("SENTRY_DNS")

if SENTRY_DNS:
    sentry_sdk.init(
        dsn=SENTRY_DNS,
        enable_tracing=True,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
