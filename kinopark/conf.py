from decouple import config

ENV_POSSIBLE_OPTIONS = ['local', 'prod']
ENV_ID = config("Kinopark_ENV", cast=str)
SECRET_KEY = 'django-insecure-&4)@vn62f(f#0movt3n3to1v*c&$3o=y2ndcn+@pc@l1(_iaki'