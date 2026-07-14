from .base import *

import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv(BASE_DIR / ".env")

DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".vercel.app",
]

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL")
    )
}

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-local-development-key"
)

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
 
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"



STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}



MIDDLEWARE.insert(
    1,
    "whitenoise.middleware.WhiteNoiseMiddleware",
)





# =====================================================
# BREVO EMAIL CONFIGURATION
# =====================================================

BREVO_API_KEY = os.environ.get("BREVO_API_KEY")

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL",
    "noreply@sjscompany.co.za"
)

ADMIN_NOTIFICATION_EMAIL = os.environ.get(
    "ADMIN_NOTIFICATION_EMAIL",
    "smangajsithole@gmail.com"
)