import os
import environ
from .base import *

# In production settings, you should focus on the security for your project.
# See https://www.apptension.com/blog-posts/how-to-configure-your-django-project-for-multiple-environments

env = environ.Env()
env.read_env()

DEBUG = False
SECRET_KEY = env("PROD_SECRET_KEY")
ALLOWED_HOSTS = ["quicklink.ph", ".quicklink.ph"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("PROD_DB_NAME"),
        "USER": env("PROD_DB_USER"),
        "PASSWORD": env("PROD_DB_PW"),
        "HOST": env("PROD_DB_HOST"),
        "PORT": env("PROD_DB_PORT"),
    }
}