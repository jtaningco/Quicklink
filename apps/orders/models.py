from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField

from apps.products.models import Product

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

    # Change user to customer once login authentication has been set
    # user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL) 
    order_date = models.DateTimeField(auto_now_add=True, null=True)

    quantity = models.IntegerField(null=True)
    # Order quantity is different from product quantity -- sum of all products na kasama
    
    total = models.IntegerField(null=True)
    order_status = models.CharField(max_length=40, null=True, choices=ORDER_STATUS)
    payment_status = models.CharField(max_length=40, null=True, choices=PAYMENT_STATUS)
    delivery_date = models.DateTimeField(null=True)
    notes = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.product.name