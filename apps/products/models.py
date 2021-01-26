from django.db import models
from django.db.models.fields import IntegerField

from apps.accounts.models import User

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=55, null=True, blank=True)

    def __str__(self):
        return self.name

# Class Size for implementation of inline formsets
# class Size(models.Model):
#     name = models.CharField(max_length=80, null=True, blank=False)
#     price = models.IntegerField(null=True, blank=False)

# Class Addon for implementation of inline formsets
# class Addon(models.Model):
#     name = models.CharField(max_length=80, null=True, blank=False)
#     price = models.IntegerField(null=True, blank=False)

class Product(models.Model):
    CHOICES=[('Made to Order','Made to Order'),
            ('1','1'),
            ('2','2'),
            ('3','3')]
            
    # tags = models.ManyToManyField(Tag)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=55, null=True, blank=False)
    description = models.CharField(max_length=100, null=True, blank=False)

    image = models.ImageField(null=True, blank=True, upload_to='media')

    stock = models.CharField(max_length=55, choices=CHOICES, null=True, default=CHOICES[0], blank=False)
    
    size = models.CharField(max_length=80, null=True, blank=False)
    price = models.IntegerField(null=True, blank=False)
    
    addon = models.CharField(max_length=80, null=True, blank=True)
    addon_price = models.IntegerField(null=True, blank=True)

    instructions = models.CharField(max_length=100, null=True, blank=True)
    
    sold = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name