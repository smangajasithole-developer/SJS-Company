from .base import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "sjscompany",
        "USER": "postgres",
        "PASSWORD": "SJsithole@990121",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-local-development-key"
)

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"