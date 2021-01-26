from django.db import models
from django.contrib.auth.models import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.

class User(AbstractUser):
    class Types(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MERCHANT = "MERCHANT", "Merchant"
        CUSTOMER = "CUSTOMER", "Customer"

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

    role = models.CharField(_('Role'), max_length=50, choices=Types.choices, default=Types.ADMIN, null=True)
    email = models.EmailField(max_length=150, null=True)
    password = models.CharField(max_length=150, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.username


class MerchantManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.MERCHANT)

class MerchantInformation(models.Model):
    user = models.OneToOneField(
        User, related_name="merchant_information", on_delete=models.CASCADE
    )
    first_name = models.CharField(_("first name"), null=True, max_length=150)
    middle_initial = models.CharField(
        _("middle initial"), max_length=10, null=True, blank=True, default=""
    )
    last_name = models.CharField(_("last name"), null=True, max_length=150)
    mobile_number = models.CharField(_("mobile number"), max_length=15, null=True)

    def __str__(self):
        if not (self.first_name) and (self.last_name):
            return self.username
        else:
            return self.first_name + " " + self.last_name

class Merchant(User):
    base_type = User.Types.MERCHANT
    objects = MerchantManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.MERCHANT
        return super().save(*args, **kwargs)


class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)

class CustomerInformation(models.Model):
    customer = models.OneToOneField(
        User, related_name="customer_information", on_delete=models.CASCADE
    )
    name = models.CharField(_("customer name"), max_length=150, null=True, blank=False)
    mobile_number = models.CharField(_("mobile number"), max_length=15, null=True, blank=False)
    instagram = models.CharField(_("instagram"), max_length=150, null=True, blank=False)
    instagram_name = models.CharField(_("instagram name"), max_length=150, null=True, blank=False)

class Customer(User):
    base_type = User.Types.CUSTOMER
    objects = CustomerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.CUSTOMER
        return super().save(*args, **kwargs)