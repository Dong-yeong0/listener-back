import os
import socket

import environ

from .base import *

env = environ.Env()

ALLOWED_HOSTS = ["localhost", "127.0.0.1", socket.gethostbyname(socket.gethostname())]

# 개발 환경에서는 CORS 모든 도메인 허용
CORS_ALLOW_ALL_ORIGINS = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }
}

DEBUG = True
LOGGING["loggers"]["core"]["handlers"] = ["console"]
LOGGING["loggers"]["core"]["level"] = "DEBUG"
LOGGING["loggers"]["apps"]["handlers"] = ["console"]
LOGGING["loggers"]["apps"]["level"] = "DEBUG"
