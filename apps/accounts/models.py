from django.db import models
from django.contrib.auth.models import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from .validators import only_int, exp_date

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

    role = models.CharField(_('role'), max_length=50, choices=Types.choices, default=Types.ADMIN, null=True)
    email = models.EmailField(max_length=150, null=True)
    password = models.CharField(max_length=150, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.username

# INFORMATION
class Address(models.Model):
    class Cities(models.TextChoices):
        CAL = "Caloocan", "Caloocan City"
        LP = "Las Piñas", "Las Piñas City"
        MKT = "Makati", "Makati City"
        MAL = "Malabon", "Malabon City"
        MND = "Mandaluyong", "Malanduyong City"
        MNL = "Manila", "Manila City"
        MAR = "Marikina", "Marikina City"
        MUN = "Muntinlupa", "Muntinlupa City"
        NAV = "Navotas", "Navotas City"
        PAR = "Parañaque", "Parañaque City"
        PSY = "Pasay", "Pasay City"
        PSG = "Pasig", "Pasig City"
        PAT = "Pateros", "Pateros City"
        QZN = "Quezon", "Quezon City"
        SJ = "San Juan", "San Juan City"
        TAG = "Taguig", "Taguig City"
        VAL = "Valenzuela", "Valenzuela City"

    line1 = models.CharField(_("address line1"), null=True, max_length=155)
    line2 = models.CharField(_("address line2"), null=True, max_length=155)
    city = models.CharField(_("address city"), choices=Cities.choices, null=True, max_length=55)
    province = models.CharField(_("address province"), null=True, max_length=55)
    postal_code = models.CharField(_("address postal code"), null=True, max_length=4, validators=[only_int])

    def __str__(self):
        return self.line1 + " " + self.line2

class SocialMediaLinks(models.Model):
    instagram = models.CharField(_("instagram link"), null=True, max_length=255)
    facebook = models.CharField(_("facebook link"), null=True, max_length=255)
    twitter = models.CharField(_("twitter link"), null=True, max_length=255)

class BankAccount(models.Model):
    class Banks(models.TextChoices):
        BPI = "BPI", "Bank of the Philippine Islands"
        BDO = "BDO", "Banco de Oro"
        GCASH = "GCash", "GCash"
        GRABPAY = "GrabPay", "GrabPay"
    
    bank_name = models.CharField(_("bank name"), choices=Banks.choices, null=True, max_length=55)
    cardholder_name = models.CharField(_("cardholder name"), choices=Banks.choices, null=True, max_length=155)
    account_number = models.CharField(_("account number"), null=True, max_length=55)
    exp_date = models.CharField(_("expiration date"), null=True, max_length=4, validators=[exp_date])
    cvv = models.CharField(_("card verification value"), null=True, max_length=3)

    def __str__(self):
        return self.account_number

class Notifications(models.Model):
    sms = models.BooleanField(_('sms notifications'), null=True, default=False)
    email = models.BooleanField(_('email notifications'), null=True, default=False)

# MERCHANT
class MerchantManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.MERCHANT)

class Merchant(User):
    base_type = User.Types.MERCHANT
    objects = MerchantManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.MERCHANT
        return super().save(*args, **kwargs)

# Days Open for Shop
class Days(models.Model):
    days = models.CharField(max_length=55, null=True, blank=True)

    def __str__(self):
        return self.days

# Shop Logo
class ShopLogo(models.Model):
    logo = models.ImageField(null=True, blank=True, upload_to='media')

# Shop Information
class ShopInformation(models.Model):
    user = models.OneToOneField(
        User, related_name="merchant_info", on_delete=models.CASCADE
    )
    shop_name = models.CharField(_("shop name"), null=True, max_length=25)
    shop_contact_number = models.CharField(_("contact number"), max_length=15, null=True)
    shop_username = models.CharField(_("shop username"), null=True, max_length=55)
    shop_days_open = models.ManyToManyField(Days)
    shop_address = models.OneToOneField(Address, related_name='shop_address', on_delete=models.CASCADE, null=True)
    shop_links = models.OneToOneField(SocialMediaLinks, related_name='shop_links', on_delete=models.CASCADE, null=True)
    shop_cod = models.BooleanField(_("shop cash on delivery"), null=True, default=False)
    shop_logo = models.OneToOneField(ShopLogo, related_name='shop_logo', on_delete=models.CASCADE, null=True)
    shop_account = models.OneToOneField(BankAccount, related_name='shop_account', on_delete=models.CASCADE, null=True)


# CUSTOMERS
class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)

class CustomerInformation(models.Model):
    customer = models.OneToOneField(
        User, related_name="customer_info", on_delete=models.CASCADE
    )
    customer_name = models.CharField(_("customer name"), max_length=150, null=True, blank=False)
    customer_mobile_number = models.CharField(_("mobile number"), max_length=15, null=True, blank=False, validators=[only_int])
    customer_links = models.OneToOneField(SocialMediaLinks, related_name='customer_links', on_delete=models.CASCADE, null=True)
    customer_address = models.OneToOneField(Address, related_name='customer_address', on_delete=models.CASCADE, null=True)
    customer_notifications = models.OneToOneField(Notifications, related_name='customer_notifs', on_delete=models.CASCADE, null=True)

class Customer(User):
    base_type = User.Types.CUSTOMER
    objects = CustomerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.CUSTOMER
        return super().save(*args, **kwargs)