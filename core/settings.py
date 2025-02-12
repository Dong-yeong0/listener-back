import os

# 기본 설정을 base.py에서 불러오기
from .configs.base import *

# 환경 변수를 확인해서 알맞은 설정을 불러오기
ENVIRONMENT = os.getenv("DJANGO_ENV", "development")

if ENVIRONMENT == "production":
    from .configs.production import *
elif ENVIRONMENT == "development":
    from .configs.development import *
else:
    raise ValueError("Invalid DJANGO_ENV value. Choose 'development' or 'production'.")
