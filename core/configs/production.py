import os

import environ

from .base import *

env = environ.Env()

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1년
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT", "5432"),
    }
}


# CORS 설정 (필요한 도메인만 허용)
CORS_ALLOWED_ORIGINS = []

DEBUG = False
LOGGING["loggers"]["core"]["handlers"] = ["file"]
LOGGING["loggers"]["core"]["level"] = "WARNING"
LOGGING["loggers"]["apps"]["handlers"] = ["file"]
LOGGING["loggers"]["apps"]["level"] = "WARNING"
