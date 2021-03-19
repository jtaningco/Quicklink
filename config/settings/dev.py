import environ
import os
from .base import *
from django.contrib.auth import authenticate, login, logout
import django.http.request

# Initialise environment variables
env = environ.Env()
env.read_env()

# Email verification settings
# See the docs for more information: https://pypi.org/project/django-email-verification/

def verified_callback(user):
    user.is_active = True
    user.save()

EMAIL_VERIFIED_CALLBACK = verified_callback
EMAIL_FROM_ADDRESS = 'josh@quicklink.ph'
EMAIL_MAIL_SUBJECT = 'Quicklink Email Verification'
EMAIL_MAIL_HTML = 'emails/verification.html'
EMAIL_MAIL_PLAIN = 'emails/verification.txt'
EMAIL_TOKEN_LIFE = 60 * 60
EMAIL_PAGE_TEMPLATE = 'accounts/email-confirmation.html'
EMAIL_PAGE_DOMAIN = env("DEV_DOMAIN")

# For Django Email Backend
# Use 'django.core.mail.backends.smtp.EmailBackend' for production
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = env("DEV_EMAIL")
EMAIL_HOST_PASSWORD = env("DEV_EMAIL_PW")
EMAIL_USE_TLS = True

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