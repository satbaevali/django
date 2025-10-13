from decouple import config

ENV_POSSIBLE_OPTIONS = ['local', 'prod']
ENV_ID = config("Kinopark_ENV", default="local", cast=str)
SECRET_KEY = config("SECRET_KEY")
