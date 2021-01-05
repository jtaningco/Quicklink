from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField

from ..accounts.models import Customer
from ..products.models import Product

# Create your models here.
class Order(models.Model):
    ORDER_STATUS = [
        ('Pending', 'Pending'),
        ('Sent', 'Sent'),
        ('Received', 'Received'),
        ('Cancelled', 'Cancelled')
    ]

    PAYMENT_STATUS = [
        ('To Receive', 'To Receive'),
        ('Processing', 'Processing'),
        ('Received', 'Received')
    ]

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL) 
    order_date = models.DateTimeField(auto_now_add=True, null=True)
    order_number = models.IntegerField(null=True)
    quantity = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    order_status = models.CharField(max_length=40, null=True, choices=ORDER_STATUS)
    payment_status = models.CharField(max_length=40, null=True, choices=PAYMENT_STATUS)
    delivery_date = models.DateTimeField(null=True)
    notes = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name