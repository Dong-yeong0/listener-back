import os

from .base import *

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# 개발 환경에서는 CORS 모든 도메인 허용
CORS_ALLOW_ALL_ORIGINS = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

DEBUG = True
LOGGING["loggers"]["core"]["handlers"] = ["console"]
LOGGING["loggers"]["core"]["level"] = "DEBUG"
LOGGING["loggers"]["apps"]["handlers"] = ["console"]
LOGGING["loggers"]["apps"]["level"] = "DEBUG"
