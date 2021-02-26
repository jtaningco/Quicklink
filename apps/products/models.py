from django.db import models
from django.db.models.fields import IntegerField

from apps.accounts.models import User

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=55, null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    # tags = models.ManyToManyField(Tag)

    # User manipulating the product (request.user — whoever is logged in)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    # Product name and description
    name = models.CharField(max_length=30, null=True, blank=False)
    description = models.CharField(max_length=100, null=True, blank=False)

    # Product images
    image = models.ImageField(null=True, blank=True)

    # Stocks available
    stock = models.CharField(max_length=15, null=True, blank=True)

    # Available delivery schedules
    schedule = models.CharField(max_length=55, null=True)

    # Order cut-off
    days = models.IntegerField(null=True, blank=False, default=0)
    time = models.CharField(max_length=10, null=True, blank=False)

    orders = models.CharField(max_length=55, null=True, blank=True)

    instructions = models.CharField(max_length=100, null=True, blank=True)
    
    sold = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.user} — {self.name}"

# Class Size for implementation of inline formsets
class Size(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    size = models.CharField(max_length=80, null=True, blank=False)
    price_size = models.IntegerField(null=True, blank=False)

    def size_to_json(self):
        return {
            "product": self.product,
            "size": self.size,
            "price_size": self.price_size,
        }

    def __str__(self):
        return f"{self.product} — {self.size}"

# Class Addon for implementation of inline formsets
class Addon(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    addon = models.CharField(max_length=80, null=True, blank=False)
    price_addon = models.IntegerField(null=True, blank=False)

    def addon_to_json(self):
        return {
            "product": self.product,
            "addon": self.addon,
            "price_addon": self.price_addon,
        }

    def __str__(self):
        return f"{self.product} — {self.addon}"