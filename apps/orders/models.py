from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField
from django.utils.timezone import datetime, timedelta

from apps.accounts.models import User
from apps.products.models import *

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

    # User manipulating the product (request.user — whoever is logged in)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="order_sender")

    # Shop getting the order
    shop = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="order_receiver")

    # Order quantity is different from product quantity -- sum of all products na kasama
    order_quantity = models.IntegerField(null=True, default=1)
    
    # Convenience fees for the order
    fees = models.DecimalField(null=True, default=0, max_digits=8, decimal_places=2)

    # Total fees for the order
    total = models.DecimalField(null=True, default=0, max_digits=10, decimal_places=2)

    # Order status
    order_status = models.CharField(max_length=40, null=True, choices=ORDER_STATUS, default='Pending')
    
    # Order payment status
    payment_status = models.CharField(max_length=40, null=True, choices=PAYMENT_STATUS, default='To Receive')
    
    # Date of when the order was published (Auto-filled)
    order_date = models.DateTimeField(auto_now_add=True, null=True)

    # Preferred delivery date of when the product will be delivered (Auto-filled)
    delivery_date = models.DateTimeField(null=True, default=datetime.today()+timedelta(days=1))

    # Check if order is complete
    complete = models.BooleanField(default=False, null=True, blank=False)

    notes = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.order_date} - Total of PHP {self.total}"

    def delivery_date(self):
        return datetime.today()+timedelta(days=3)

class ProductOrder(models.Model):
    # Order cart
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL) 

    # Product ordered
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

    # Product size
    size = models.ForeignKey(Size, null=True, on_delete=models.CASCADE)
    
    # Product addons
    addons = models.ManyToManyField(Addon, blank=True)  
    
    # Product quantity ordered
    quantity = models.IntegerField(null=True, default=1)

    # Special instructions per order
    instructions = models.CharField(max_length=140, null=True, blank=True)
    
    # Total product fees (Auto-filled in views.py under updateItem, line 265)
    total = models.DecimalField(null=True, default=0, max_digits=8, decimal_places=2)

    # Date of when the order was published (Auto-filled)
    order_date = models.DateTimeField(auto_now_add=True, null=True)
    

    def __str__(self):
        return f"{self.quantity} {self.product} - Total of PHP {self.total}" 