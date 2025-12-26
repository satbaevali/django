from decouple import config
from django.core.exceptions import ImproperlyConfigured


ENV_POSSIBLE_OPTIONS = ['local', 'prod']

ENV_ID = config("settings_ENV", default="local", cast=str)


if ENV_ID not in ENV_POSSIBLE_OPTIONS:
    raise ImproperlyConfigured(f"Invalid settings_ENV value: {ENV_ID}")

SECRET_KEY = config("SECRET_KEY", default="django-insecure-&4)@vn62f(f#0movt3n3to1v*c&$3o=y2ndcn+@pc@l1(_iaki")
