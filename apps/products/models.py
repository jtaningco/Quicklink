from django.db import models
from django import forms
from django.db.models.fields import IntegerField

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=55, null=True, blank=True)

    def __str__(self):
        return self.name

class Stock(models.Model):
    stock = models.CharField(max_length=80, null=True, blank=False)
    size = models.CharField(max_length=80, null=True, blank=False)

class Product(models.Model):
    CHOICES=[('Made to Order','Made to Order'),
            ('1','1'),
            ('2','2'),
            ('3','3')]

    tags = models.ManyToManyField(Tag)
    name = models.CharField(max_length=55, null=True, blank=False)
    description = models.CharField(max_length=100, null=True, blank=False)
    productImage = models.ImageField(null=True, blank=True)
    stock = models.CharField(max_length=55, choices=CHOICES, null=False, default=CHOICES[0], blank=False)
    size = models.CharField(max_length=80, null=True, blank=False)
    price = models.IntegerField(null=True, blank=False)
    addon = models.CharField(max_length=80, null=True, blank=True)
    instructions = models.CharField(max_length=100, null=True, blank=True)
    
    sold = models.IntegerField(null=True, blank=False, default=0)

    def __str__(self):
        return self.name