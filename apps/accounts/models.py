from django.db import models
from django.contrib.auth.models import UnicodeUsernameValidator, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from .validators import only_int, exp_date

import shortuuid
from shortuuidfield import ShortUUIDField

from imagekit import ImageSpec, register
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

### Create your models here.
## Django Roles, Permissions, and Groups: https://medium.com/djangotube/django-roles-groups-and-permissions-introduction-a54d1070544
## Django Custom Authentication: https://docs.djangoproject.com/en/3.1/topics/auth/customizing/

##### SUMMARY OF ACCOUNT MODELS:
#### Super Admin — Quicklink High-Ranking Programmers (CRUD All)
### Admin — Quicklink Founders, High-Ranking Employees, and Programmers (CUD Some, R All)
## Staff — Quicklink Employees
# Merchants — Quicklink Clients / Users ()
# Customers — Customers of Quicklink Clients

class MyUserManager(BaseUserManager):
    ## A custom user manager to deal with emails as unique identifiers for auth
    # instead of usernames. The default that's used is "UserManager"

    def create_user(self, email, password, **extra_fields):
        # Creates and saves a User with the given email and password.
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
        ADMIN = "ADMIN", "Admin"
        QUICKIES = "QUICKIES", "Quickies"
        MERCHANT = "MERCHANT", "Merchant"
        CUSTOMER = "CUSTOMER", "Customer"

    id = ShortUUIDField(primary_key=True, max_length=15, blank=True, editable=False)

    role = models.CharField(_('role'), max_length=50, choices=Types.choices, default=Types.ADMIN, null=True)
    
    username = None
    email = models.EmailField(_("email address"), 
        max_length=150, 
        null=True, 
        unique=True,
        help_text=_("Please use a business email address."),
        error_messages={"unique": _("That email is already being used by another account."),},
    )

    password = models.CharField(max_length=150, null=True)

    device_id = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'password']
    
    objects = MyUserManager()

    def __str__(self):
        if self.email:
            return f"{self.email}"
        elif self.device_id:
            return f"{self.device_id}"

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_initials(self):
        initials = []
        if hasattr(self, 'shop_info'):
            for name in list(self.shop_info.shop_name.split(' ')):
                initials.append(name[0])
            return ''.join(initials)
        elif hasattr(self, 'info_customer'):
            for name in list(self.info_customer.customer_name.split(' ')):
                initials.append(name[0])
            return ''.join(initials)
        else:
            return False

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
    line1 = models.CharField(_("address line1"), null=True, blank=False, max_length=155)
    line2 = models.CharField(_("address line2"), null=True, blank=True, max_length=155)
    city = models.CharField(_("address city"), choices=CITIES, null=True, blank=False, max_length=55, default=None)
    province = models.CharField(_("address province"), choices=PROVINCES, null=True, blank=False, max_length=55, default=None)
    postal_code = models.CharField(_("address postal code"), null=True, max_length=4, blank=False, validators=[only_int])

    def __str__(self):
        return f"{self.line1}, {self.line2}, {self.city}, {self.province}, Philippines, {self.postal_code}"

# Social Media Links
class SocialMediaLink(models.Model):
    user = models.OneToOneField(User, related_name='user_links', on_delete=models.CASCADE, null=True, blank=True)
    instagram = models.CharField(_("instagram link"), null=True, default="", max_length=255)
    facebook = models.CharField(_("facebook link"), null=True, default="", max_length=255)
    twitter = models.CharField(_("twitter link"), null=True, default="", max_length=255)

    def __str__(self):
        accounts = []
        if self.instagram: accounts.append('Instagram')
        if self.facebook: accounts.append('Facebook')
        if self.twitter: accounts.append('Twitter')
        if len(accounts) == 0:
            return "No social media accounts"
        return f"Linked social media accounts: {', '.join(accounts)}"

# Bank Account Information
class BankAccount(models.Model):
    BANKS = [
        ('', 'Choose bank / e-wallet'),
        ("BPI", _("Bank of the Philippine Islands (BPI)")),
        ("BDO", _("Banco de Oro (BDO)")),
        ("UB", _("UnionBank PH")),
        ("GCash", _("GCash PH")),
        ("PayMaya", _("PayMaya PH")),
        ("GrabPay", _("GrabPay")),
    ]
    
    user = models.OneToOneField(User, related_name='user_account', on_delete=models.SET_NULL, null=True)
    bank_name = models.CharField(_("bank name"), choices=BANKS, null=True, max_length=55)
    cardholder_name = models.CharField(_("cardholder name"), null=True, max_length=155)
    account_number = models.CharField(_("account number"), null=True, max_length=55)
    exp_date = models.CharField(_("expiration date"), null=True, max_length=5, validators=[exp_date])
    cvv = models.CharField(_("card verification value"), null=True, max_length=3)

    def get_first_four(self):
        first_four_list = []
        for i in range(len(account_number)):
            if i >= 4:
                first_four_list.append(i)
        first_four = ' '.join([str(i) for i in first_four_list])
        return f"{self.first_four}"

    def get_second_four(self):
        second_four_list = []
        for i in range(len(account_number)):
            if i < 4 and i >= 8:
                second_four_list.append(i)
        second_four = ' '.join([str(i) for i in second_four_list])
        return f"{self.second_four}"

    def get_third_four(self):
        third_four_list = []
        for i in range(len(account_number)):
            if i < 4 and i >= 8:
                third_four_list.append(i)
        third_four = ' '.join([str(i) for i in third_four_list])
        return f"{self.third_four}"

    def get_last_four(self):
        last_four_list = []
        for i in range(len(account_number)):
            if i < 4 and i >= 8:
                last_four_list.append(i)
        last_four = ' '.join([str(i) for i in last_four_list])
        return f"{self.last_four}"

    def __str__(self):
        return f"{self.cardholder_name} - {self.account_number}"

class Notification(models.Model):
    user = models.OneToOneField(User, related_name='customer_notifications', on_delete=models.CASCADE, null=True, blank=True)
    sms = models.BooleanField(_('sms notifications'), null=True, default=False)
    email = models.BooleanField(_('email notifications'), null=True, default=False)

    def __str__(self):
        return f"SMS: {self.sms} | Email: {self.email}"

# MERCHANT
# class MerchantManager(models.Manager):
#     def get_queryset(self, *args, **kwargs):
#         return super().get_queryset(*args, **kwargs).filter(type=User.Types.MERCHANT)

# class Merchant(User):
#     base_type = User.Types.MERCHANT
#     objects = MerchantManager()

#     class Meta:
#         proxy = True

#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.type = User.Types.MERCHANT
#         return super().save(*args, **kwargs)

# Shop Information
class ShopInformation(models.Model):
    user = models.OneToOneField(
        User, related_name="shop_info", on_delete=models.CASCADE
    )
    shop_name = models.CharField(_("shop name"), null=True, max_length=30)
    shop_contact_number = models.CharField(_("contact number"), max_length=15, null=True)
    shop_username = models.CharField(_("shop username"), 
        max_length=150, 
        null=True, 
        unique=True, 
        help_text=_(
            "This will be used for your order form link (quicklink.ph/username)."
        ),
        error_messages={"unique": _("A user with that username already exists."),},
    )
    shop_email = models.EmailField(_("email address"), 
        max_length=150, 
        null=True,
        help_text=_(
            "Your customers will contact you through this email address."
        ),
    )
    shop_delivery_fees = models.DecimalField(null=True, blank=False, max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.shop_username} - {self.shop_name} ({self.shop_contact_number})"

# Available Delivery Schedule
# See more information on how to do it here: https://stackoverflow.com/questions/3663898/representing-a-multi-select-field-for-weekdays-in-a-django-model

class BitChoices(object):
  def __init__(self, choices):
    self._choices = []
    self._lookup = {}
    for index, (key, val) in enumerate(choices):
      index = 2**index
      self._choices.append((index, val))
      self._lookup[key] = index

  def __iter__(self):
    return iter(self._choices)

  def __len__(self):
    return len(self._choices)

  def __getattr__(self, attr):
    try:
      return self._lookup[attr]
    except KeyError:
      raise AttributeError(attr)

  def get_selected_keys(self, selection):
    # Return a list of keys for the given selection
    return [ k for k,b in self._lookup.iteritems() if b & selection]

  def get_selected_values(self, selection):
    # Return a list of values for the given selection
    return [ v for b,v in self._choices if b & selection]

WEEKDAYS = BitChoices((
    ('Mon', 'Monday'), ('Tues', 'Tuesday'), ('Wed', 'Wednesday'),
    ('Thurs', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'),
    ('Sun', 'Sunday')
))

# General Shop Settings
class ShopGeneralSettings(models.Model):
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
        (i,f"{i-12}:00 PM") for i in range(13,24)
    ]

    shop = models.OneToOneField(ShopInformation, related_name='shop_general_settings', on_delete=models.CASCADE, null=True, blank=True)
    shop_cod = models.BooleanField(_("shop cash on delivery"), null=True, blank=True, default=False)

    # Order cut-off
    cutoff_days = models.IntegerField(null=True, blank=False, default=0)
    cutoff_time = models.CharField(max_length=10, null=True, blank=False)

    # Delivery days
    delivery_days = models.PositiveIntegerField(choices=WEEKDAYS, null=True, blank=False)
    delivery_everyday = models.BooleanField(_("everyday delivery"), null=True, default=False)

    # Delivery hours
    delivery_from_hour = models.PositiveSmallIntegerField(choices=HOUR_OF_DAY_24, null=True, default=None)
    delivery_to_hour = models.PositiveSmallIntegerField(choices=HOUR_OF_DAY_24, null=True, default=None)

    def __str__(self):
        return f"{self.shop.shop_name}"

# General Shop Settings
class ShopDeliverySettings(models.Model):
    shop = models.OneToOneField(ShopInformation, related_name='shop_delivery_settings', on_delete=models.CASCADE, null=True, blank=True)
    seller_books = models.BooleanField(_("seller books"), blank=True, null=True, default=False)
    buyer_books = models.BooleanField(_("buyer books"), blank=True, null=True, default=False)
    buyer_picks_up = models.BooleanField(_("buyer picks up"), blank=True, null=True, default=False)

    line1 = models.CharField(_("delivery line1"), null=True, blank=True, max_length=155, default="Address Line 1")
    line2 = models.CharField(_("delivery line2"), null=True, blank=True, max_length=155, default="Address Line 2")
    city = models.CharField(_("delivery city"), choices=Address.CITIES, null=True, blank=True, max_length=55, default=Address.CITIES[0])
    province = models.CharField(_("delivery province"), choices=Address.PROVINCES, null=True, blank=True, max_length=55, default=Address.PROVINCES[0])
    postal_code = models.CharField(_("delivery postal code"), null=True, max_length=4, blank=True, validators=[only_int], default="0000")

    def __str__(self):
        return f"{self.shop.shop_name}"

# Shop Open Hours
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

    shop = models.OneToOneField(ShopInformation, related_name='open_hours_shop', on_delete=models.CASCADE, null=True, blank=True)
    day_from = models.PositiveSmallIntegerField(choices=WEEKDAYS, null=True, default=None)
    day_to = models.PositiveSmallIntegerField(choices=WEEKDAYS, null=True, default=None)
    from_hour = models.PositiveSmallIntegerField(choices=HOUR_OF_DAY_24, null=True, default=None)
    to_hour = models.PositiveSmallIntegerField(choices=HOUR_OF_DAY_24, null=True, default=None)
    # always_open = models.BooleanField(_("shop 24/7"), null=True, default=False)

    def get_day_from(self):
        return OpenHours.WEEKDAYS[self.day_from]

    def get_day_to(self):
        return OpenHours.WEEKDAYS[self.day_to] 

    def get_from_hour(self):
        return OpenHours.HOUR_OF_DAY_24[self.from_hour]

    def get_to_hour(self):
        return OpenHours.HOUR_OF_DAY_24[self.to_hour]

    def __str__(self):
        return f"{self.day_from} ({self.from_hour}) - {self.day_to} ({self.to_hour})"

# Shop Logo
class Avatar(ImageSpec):
    processors = [ResizeToFit(16, 16)]
    format = 'JPEG'
    options = {'quality': 75}

register.generator('account:avatar', Avatar)

class ShopLogo(models.Model):
    shop = models.OneToOneField(ShopInformation, related_name='shop_logo', on_delete=models.CASCADE, null=True, blank=True)
    logo = models.ImageField(upload_to='%Y/%m/%d/shop_logos', null=True, blank=True)
    logo_avatar = ImageSpecField(source='logo', processors=[ResizeToFit(16, 16)], format='JPEG', options={'quality': 75})

    def __str__(self):
        return f"URL: {self.logo}"

# CUSTOMERS
# class CustomerManager(models.Manager):
#     def get_queryset(self, *args, **kwargs):
#         return super().get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)

# class Customer(User):
#     base_type = User.Types.CUSTOMER
#     objects = CustomerManager()

#     class Meta:
#         proxy = True

#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.type = User.Types.CUSTOMER
#         return super().save(*args, **kwargs)

class CustomerInformation(models.Model):
    customer = models.OneToOneField(
        User, related_name="info_customer", on_delete=models.CASCADE, null=True
    )

    customer_name = models.CharField(_("customer name"), max_length=150, null=True, blank=False)
    customer_email = models.EmailField(_("email"), 
        max_length=150, 
        null=True,
    )
    customer_contact_number = models.CharField(_("mobile number"), max_length=15, null=True, blank=False, validators=[only_int])
    customer_username = models.CharField(_("customer username"), 
        max_length=150, 
        null=True, 
        unique=True, 
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only."
        ),
        error_messages={"unique": _("A user with that username already exists."),},
    )

    def __str__(self):
        return f"{self.customer_username} - {self.customer_name} ({self.customer_contact_number})"