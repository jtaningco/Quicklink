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
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="order_sender")

    # Shop getting the order
    shop = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="order_receiver")

    # Order quantity is different from product quantity -- sum of all products na kasama
    order_quantity = models.IntegerField(null=True, default=1)
    
    # Total fees for the order
    total = models.DecimalField(null=True, default=0, max_digits=10, decimal_places=2)

    # Order status
    order_status = models.CharField(max_length=40, null=True, choices=ORDER_STATUS, default='Pending')
    
    # Order payment status
    payment_status = models.CharField(max_length=40, null=True, choices=PAYMENT_STATUS, default='To Receive')
    
    # Date of when the order was published (Auto-filled)
    order_date = models.DateTimeField(auto_now_add=True, null=True)

    notes = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.order_date} - Total of PHP {self.total}"

class ProductOrder(models.Model):
    # Order cart
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE) 

    # Product ordered
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)

    # Product size
    size = models.ForeignKey(Size, null=True, on_delete=models.CASCADE)
    
    # Product addons
    addons = models.ManyToManyField(Addon, blank=True)  
    
    # Product quantity ordered
    quantity = models.IntegerField(null=True, default=1)

    # Special instructions per order
    instructions = models.CharField(max_length=140, null=True, blank=True)
    
    # Total product fees (Auto-filled)
    total = models.DecimalField(null=True, default=0, max_digits=8, decimal_places=2)

    # Date of when the order was published (Auto-filled)
    order_date = models.DateTimeField(auto_now_add=True, null=True)

    # Date of when the product will be delivered (Auto-filled)
    delivery_date = models.DateTimeField(null=True, default=datetime.today()+timedelta(days=1))
    

    def __str__(self):
        return f"{self.order} - {self.quantity} {self.product}" 

    def total(self):
        if addons:
            addons_total = 0
            for i in addons:
                addons_total += i.price_addon
            return (self.quantity * self.size.price_size) + addons_total
        else:    
            return self.quantity * self.size.price_size

    def delivery_date(self):
        return datetime.today()+timedelta(days=self.product.days)