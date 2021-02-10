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

    role = models.CharField(_('role'), max_length=50, choices=Types.choices, default=Types.ADMIN, null=True)
    username = models.CharField(_("username"), 
        max_length=150, 
        null=True, 
        unique=True, 
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only."
        ),
        error_messages={"unique": _("A user with that username already exists."),},
    )
    email = models.EmailField(_("email"), 
        max_length=150, 
        null=True, 
        unique=True,
        error_messages={"unique": _("That email is already being used by another account."),},
    )
    password = models.CharField(max_length=150, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.email

# ACCOUNT INFORMATION
# Address
class Address(models.Model):
    CITIES = [
        ("Caloocan City", _("Caloocan")),
        ("Las Piñas City", _("Las Piñas")),
        ("Makati City", _("Makati")),
        ("Malabon City", _("Malabon")),
        ("Malanduyong City", _("Malanduyong")),
        ("Manila City", _("Manila")),
        ("Marikina City", _("Marikina")),
        ("Muntinlupa City", _("Muntinlupa")),
        ("Navotas City", _("Navotas")),
        ("Parañaque City", _("Parañaque")),
        ("Pasay City", _("Pasay")),
        ("Pasig City", _("Pasig")),
        ("Pateros City", _("Pateros")),
        ("Quezon City", _("Quezon City")),
        ("San Juan City", _("San Juan")),
        ("Taguig City", _("Taguig")),
        ("Valenzuela City", _("Valenzuela")),
    ]

    PROVINCES = [
        ("Metro Manila", _("Metro Manila")),
    ]

    user = models.OneToOneField(User, related_name='user_address', on_delete=models.CASCADE, null=True, blank=True)
    line1 = models.CharField(_("address line1"), null=True, max_length=155)
    line2 = models.CharField(_("address line2"), null=True, max_length=155)
    city = models.CharField(_("address city"), choices=CITIES, null=True, max_length=55, default=None)
    province = models.CharField(_("address province"), choices=PROVINCES, null=True, max_length=55, default=None)
    postal_code = models.CharField(_("address postal code"), null=True, max_length=4, validators=[only_int])

    def __str__(self):
        return f"{self.line1} {self.line2}"

# Social Media Links
class SocialMediaLinks(models.Model):
    user = models.OneToOneField(User, related_name='user_links', on_delete=models.CASCADE, null=True, blank=True)
    instagram = models.CharField(_("instagram link"), null=True, max_length=255)
    facebook = models.CharField(_("facebook link"), null=True, max_length=255)
    twitter = models.CharField(_("twitter link"), null=True, max_length=255)

# Bank Account Information
class BankAccount(models.Model):
    BANKS = [
        ("Bank of the Philippine Islands", _("BPI")),
        ("Banco de Oro", _("BDO")),
        ("Gcash", _("GCash")),
        ("GrabPay", _("GrabPay")),
    ]
    
    user = models.OneToOneField(User, related_name='user_account', on_delete=models.CASCADE, null=True, blank=True)
    bank_name = models.CharField(_("bank name"), choices=BANKS, null=True, max_length=55)
    cardholder_name = models.CharField(_("cardholder name"), null=True, max_length=155)
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

# Shop Information
class ShopInformation(models.Model):
    user = models.OneToOneField(
        User, related_name="info_shop", on_delete=models.CASCADE
    )
    shop_name = models.CharField(_("shop name"), null=True, max_length=25)
    shop_contact_number = models.CharField(_("contact number"), max_length=15, null=True)
    shop_username = models.CharField(_("shop username"), 
        max_length=150, 
        null=True, 
        unique=True, 
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only."
        ),
        error_messages={"unique": _("A user with that username already exists."),},
    )
    shop_cod = models.BooleanField(_("shop cash on delivery"), null=True, default=False)

    def __str__(self):
        return f"{self.shop_name} - {self.shop_username}"

# Available Delivery Schedule
class OpenHours(models.Model):
    HOUR_OF_DAY_24 = [
        (0, "12:00 AM"),
    ]

    HOUR_OF_DAY_24 += [
        (i,f"{i}:00 AM") for i in range(1,12)
    ]

    HOUR_OF_DAY_24 += [
        (12, "12:00 PM"),
    ]

    HOUR_OF_DAY_24 += [
        (i,f"{i-12}:00 PM") for i in range(13,25)
    ]

    WEEKDAYS = [
        (1, _("Monday")),
        (2, _("Tuesday")),
        (3, _("Wednesday")),
        (4, _("Thursday")),
        (5, _("Friday")),
        (6, _("Saturday")),
        (7, _("Sunday")),
    ]

    shop = models.OneToOneField(ShopInformation, on_delete=models.CASCADE, null=True, blank=True)
    day_from = models.PositiveSmallIntegerField(choices=WEEKDAYS, null=True, default=None)
    day_to = models.PositiveSmallIntegerField(choices=WEEKDAYS, null=True, default=None)
    from_hour = models.PositiveSmallIntegerField(choices=HOUR_OF_DAY_24, null=True, default=None)
    to_hour = models.PositiveSmallIntegerField(choices=HOUR_OF_DAY_24, null=True, default=None)
    # always_open = models.BooleanField(_("shop 24/7"), null=True, default=False)

    def get_weekday_from_display(self):
        return WEEKDAYS[self.day_from]

    def get_weekday_to_display(self):
        return WEEKDAYS[self.day_to] 

    def __str__(self):
        return f"{self.day_from} - {self.day_to}"

# Shop Logo
class ShopLogo(models.Model):
    shop = models.OneToOneField(ShopInformation, related_name='logo_shop', on_delete=models.CASCADE, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True, upload_to='logos')

# CUSTOMERS
class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)

class CustomerInformation(models.Model):
    customer = models.OneToOneField(
        User, related_name="customer_info", on_delete=models.CASCADE
    )
    customer_username = models.CharField(_("customer username"), 
        max_length=150, 
        null=True, 
        unique=True, 
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only."
        ),
        error_messages={"unique": _("A user with that username already exists."),},
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