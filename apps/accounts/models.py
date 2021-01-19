from django.db import models
from django.contrib.auth.models import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(AbstractUser):
    username = models.CharField(_("name"), 
        max_length=150, 
        null=True, 
        unique=True, 
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator(),],
        error_messages={"unique": _("A user with that username already exists."),},
        )

    email = models.EmailField(max_length=150, null=True)
    password = models.CharField(max_length=150, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    username = models.CharField(_("name"), 
        max_length=150, 
        null=True, 
        unique=True, 
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator(),],
        error_messages={"unique": _("A user with that username already exists."),},
        )
    email = models.EmailField(max_length=150, null=True)
    password = models.CharField(max_length=150, null=True)

class UserInformation(models.Model):
    user = models.OneToOneField(
        User, related_name="user_information", on_delete=models.CASCADE
    )
    first_name = models.CharField(_("first name"), null=True, max_length=150)
    middle_initial = models.CharField(
        _("middle initial"), max_length=10, null=True, blank=True, default=""
    )
    last_name = models.CharField(_("last name"), null=True, max_length=150)
    mobile_number = models.CharField(_("mobile number"), max_length=15, null=True)

class CustomerInformation(models.Model):
    customer = models.OneToOneField(
        Customer, related_name="customer_information", on_delete=models.CASCADE
    )
    name = models.CharField(_("customer name"), max_length=150, null=True, blank=False)
    mobile_number = models.CharField(_("mobile number"), max_length=15, null=True, blank=False)
    instagram = models.CharField(_("instagram"), max_length=150, null=True, blank=False)
    instagram_name = models.CharField(_("instagram name"), max_length=150, null=True, blank=False)