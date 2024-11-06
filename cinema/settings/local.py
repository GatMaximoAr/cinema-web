from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-!pak$%6f2s4o&9^3(3n_c#fis)#138j&vo27xgz3op_bjw!wf("

ALLOWED_HOSTS = []
DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": root._absolute_join("db.sqlite3"),
    }
}

# Email Settings Mailcrab
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"  
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_HOST_USER = ""  # Not authentication required
EMAIL_HOST_PASSWORD = ""
DEFAULT_FROM_EMAIL = "webmaster@localhost"