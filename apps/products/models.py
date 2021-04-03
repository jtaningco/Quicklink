from django.db import models
from django.db.models.fields import IntegerField

from apps.accounts.models import User

import shortuuid
from shortuuidfield import ShortUUIDField

from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill
import pdb

# Create your models here.
# class Tag(models.Model):
#     name = models.CharField(max_length=55, null=True, blank=True)

#     def __str__(self):
#         return self.name

class Product(models.Model):
    # Product UUID
    id = ShortUUIDField(primary_key=True, max_length=15, blank=True, editable=False)

    # Product ID (According to Shop)
    product_id = models.PositiveIntegerField(null=True, default=0)

    # User manipulating the product (request.user — whoever is logged in)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="shop_product")

    # Product name and description
    name = models.CharField(max_length=30, null=True, blank=False)
    description = models.CharField(max_length=140, null=True, blank=False)

    # Stocks available
    made_to_order = models.BooleanField(null=True, blank=True, default=False)
    stock = models.PositiveIntegerField(null=True, blank=True, default=0)

    # Maximum number of orders
    no_order_limit = models.BooleanField(null=True, blank=True, default=False)
    orders = models.PositiveIntegerField(null=True, blank=True, default=0)

    instructions = models.CharField(max_length=140, null=True, blank=True, default="")
    
    # Cheapest and highest prices
    min_price = models.CharField(max_length=25, null=True, blank=True)
    max_price = models.CharField(max_length=25, null=True, blank=True)

    # Product is active / available
    active = models.BooleanField(null=True, blank=True, default=True)

    # Number of orders sold
    sold = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self):
        if hasattr(self.user, "shop_info"):
            return f"{self.user.shop_info.shop_name} — {self.name}"
        else:
            return f"{self.name}"

    def save(self, *args, **kwargs):
        self.product_list = Product.objects.order_by('product_id')
        if len(self.product_list) == 0:
            self.product_id = 1
        else:
            self.product_id = self.product_list.last().product_id + 1
        super(Product, self).save()

    @property
    def is_made_to_order(self):
        return self.made_to_order is True

    @property
    def has_no_order_limit(self):
        return self.no_order_limit is True

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
    return f"%Y/%m/%d/products/{name}.{filename.split('.')[-1]}"

# Class Image for implementation of inline formsets
class Image(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=80, null=True, blank=True, verbose_name='Image Name')
    image = models.ImageField(upload_to="%Y/%m/%d/products/", null=True, blank=True, verbose_name='Image')
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