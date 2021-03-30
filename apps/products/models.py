from django.db import models
from django.db.models.fields import IntegerField

from apps.accounts.models import User
from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill
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

# Product Thumbnails
class Thumbnail(ImageSpec):
    processors = [ResizeToFill(320, 176)]
    format = 'JPEG'
    options = {'quality': 80}

register.generator('products:thumbnail', Thumbnail)

# Carousel / Slider Images
class Carousel(ImageSpec):
    processors = [ResizeToFill(600, 176)]
    format = 'JPEG'
    options = {'quality': 100}

register.generator('products:carousel', Carousel)

def get_image_filename(instance, filename):
    name = instance.product.name
    return "%Y/%m/%d/products/%s" % (name)

# Class Image for implementation of inline formsets
class Image(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=80, null=True, blank=True, verbose_name='Image Name')
    image = models.ImageField(upload_to=get_image_filename, null=True, blank=True, verbose_name='Image')
    default = models.BooleanField(default=False, verbose_name='Default')

    @property
    def get_product_name(self):
        name = self.product.name
        name = name.lower()
        name = name.replace(" ", "_")
        name = name + f"_{self.id}"
        return name

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

    @property
    def addon_to_json(self):
        return {
            "product": self.product,
            "addon": self.addon,
            "price_addon": self.price_addon,
        }

    def __str__(self):
        return f"{self.addon} (+ PHP {self.price_addon})"