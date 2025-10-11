"""
ASGI config for kinopark project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from kinopark.conf import ENV_POSSIBLE_OPTIONS,ENV_ID
assert ENV_ID in ENV_POSSIBLE_OPTIONS, f"Set correct Kinopark_ENV env variable. Possible options: {ENV_POSSIBLE_OPTIONS}"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kinopark.settings')

application = get_asgi_application()
