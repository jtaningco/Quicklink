from django.db import models
from django.db.models.fields import IntegerField

from apps.accounts.models import User
import pdb

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=55, null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    # tags = models.ManyToManyField(Tag)

    # User manipulating the product (request.user — whoever is logged in)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="shop_product")

    # Product name and description
    name = models.CharField(max_length=30, null=True, blank=False)
    description = models.CharField(max_length=100, null=True, blank=False)

    # Product images (upload to external image hosting site, get URLs)
    image = models.ImageField(upload_to ='uploads/', null=True, blank=True)

    # Stocks available
    stock = models.CharField(max_length=55, null=True, blank=True, default=0)

    # Maximum number of orders
    orders = models.PositiveIntegerField(null=True, blank=True, default=0)

    instructions = models.CharField(max_length=125, null=True, blank=True, default="")
    
    # Cheapest and Highest Prices
    min_price = models.CharField(max_length=25, null=True, blank=True)
    max_price = models.CharField(max_length=25, null=True, blank=True)

    # Number of orders sold
    sold = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.name}"

# Class Size for implementation of inline formsets
class Size(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    size = models.CharField(max_length=80, null=True, blank=False)
    price_size = models.DecimalField(null=True, blank=False, max_digits=6, decimal_places=2)

    @property
    def size_to_json(self):
        return {
            "product": self.product,
            "size": self.size,
            "price_size": self.price_size,
        }

    def __str__(self):
        return f"{self.size} (PHP {self.price_size})"

# Class Addon for implementation of inline formsets
class Addon(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    addon = models.CharField(max_length=80, null=True, blank=False)
    price_addon = models.DecimalField(null=True, blank=False, max_digits=5, decimal_places=2)

    def addon_to_json(self):
        return {
            "product": self.product,
            "addon": self.addon,
            "price_addon": self.price_addon,
        }

    def __str__(self):
        return f"{self.addon} (+ PHP {self.price_addon})"