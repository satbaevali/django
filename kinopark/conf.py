# Standard Library
from decouple import config

# ----------------------------------------------
# Env id
#
ENV_POSSIBLE_OPTIONS = (
    "local",
    "prod",
)
ENV_ID = config("DJANGORLAR_ENV_ID", cast=str)
SECRET_KEY = 'django-insecure-&4)@vn62f(f#0movt3n3to1v*c&$3o=y2ndcn+@pc@l1(_iaki'
