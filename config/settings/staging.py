import environ
import os
from .base import *

env = environ.Env()
env.read_env()

DEBUG = False
SECRET_KEY = env("DEV_SECRET_KEY")
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(os.path.join(BASE_DIR, "db.sqlite3"))
    }
}

# SECRET_KEY = env("STAGING_SECRET_KEY")

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": env("STAGING_DB_NAME"),
#         "USER": env("STAGING_DB_USER"),
#         "PASSWORD": env("STAGING_DB_PW"),
#         "HOST": env("STAGING_DB_HOST"),
#         "PORT": env("STAGING_DB_PORT"),
#     }
# }