import environ
import os
from .base import *

env = environ.Env()
env.read_env()


SECRET_KEY = env("DEV_SECRET_KEY")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(os.path.join(BASE_DIR, "db.sqlite3"))
    }
}

# SECRET_KEY = env("DEV_SECRET_KEY")

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": env("DEV_DB_NAME"),
#         "USER": env("DEV_DB_USER"),
#         "PASSWORD": env("DEV_DB_PW"),
#         "HOST": env("DEV_DB_HOST"),
#         "PORT": env("DEV_DB_PORT"),
#     }
# }