#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import environ


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    
    ENVIRONMENT = os.environ.get('DJANGO_ENV', 'development')
    if ENVIRONMENT == "production":
        environ.Env().read_env('.env.production')
    elif ENVIRONMENT == "development":
        environ.Env().read_env('.env.development')
    else:
        raise ValueError("Invalid DJANGO_ENV value. Choose 'development' or 'production'.")
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
