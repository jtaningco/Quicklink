from django.db import models
from django import forms
from django.db.models.fields import IntegerField

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100)
    productImage = models.ImageField(null=True, blank=True)
    stock = forms.ChoiceField(choices="Made to Order", widget=forms.RadioSelect) # Include Input in views for integer string
    size = models.CharField(max_length=40)
    price = models.IntegerField()
    addon = models.CharField(max_length=40)
    instructions = models.CharField(max_length=100)
