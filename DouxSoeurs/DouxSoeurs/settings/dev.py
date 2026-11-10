from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-zg451b779rc4+p=#_d6b$)$d-3ufkgboyi6qt&xbj%)3*0oue("

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}

try:
    from .local import *
except ImportError:
    pass
