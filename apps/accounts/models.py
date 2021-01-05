from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.

# class User(AbstractUser):
#     username = models.CharField(
#         _("username"),
#         max_length=150,
#         unique=True,
#         help_text=_(
#             "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
#         ),
#         validators=[UnicodeUsernameValidator(), MinLengthValidator(6)],
#         error_messages={"unique": _("A user with that username already exists."),},
#     )