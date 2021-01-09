from django.db import models
# from django.contrib.auth.models import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
# class User(models.Model):
#     username = models.CharField(
#         max_length=200, 
#         null=True,
#         unique=True,
#         help_text=_(
#             "Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only."
#         ),
#         validators=[UnicodeUsernameValidator(),],
#         error_messages={"unique": _("A user with that username already exists."),},
#         )

class User(models.Model):
    name = models.CharField(_("name"), max_length=150, null=True)
    mobile_number = models.CharField(_("mobile number"), max_length=15, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name