import os
import environ
from .base import *


env = environ.Env()
env.read_env()

django_heroku.settings(locals())

DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(os.path.join(BASE_DIR, "db.sqlite3"))
    }
}

# SECRET_KEY = env("PROD_SECRET_KEY")

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": env("PROD_DB_NAME"),
#         "USER": env("PROD_DB_USER"),
#         "PASSWORD": env("PROD_DB_PW"),
#         "HOST": env("PROD_DB_HOST"),
#         "PORT": env("PROD_DB_PORT"),
#     }
# }