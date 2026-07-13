from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# =====================================================
# BREVO EMAIL CONFIGURATION
# =====================================================

BREVO_API_KEY = os.environ.get(
    "BREVO_API_KEY",
    "YOUR_LOCAL_BREVO_KEY"
)

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL",
    "smangajsithole@gmail.com"
)