from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField
from django.utils.timezone import datetime, timedelta

from apps.accounts.models import *
from apps.products.models import *
import uuid

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
    
    # Subtotal for the order
    subtotal = models.DecimalField(null=True, default=0, max_digits=10, decimal_places=2)

    # Convenience fees for the order
    fees = models.DecimalField(null=True, default=0, max_digits=8, decimal_places=2)

    # Total fees for the order
    total = models.DecimalField(null=True, default=0, max_digits=12, decimal_places=2)

    # Order status
    order_status = models.CharField(max_length=40, null=True, choices=ORDER_STATUS, default='Pending')
    
    # Order payment status
    payment_status = models.CharField(max_length=40, null=True, choices=PAYMENT_STATUS, default='To Receive')
    
    # Date of when the order was published (Auto-filled)
    order_date = models.DateTimeField(auto_now_add=True, null=True)

    # Preferred delivery date of when the product will be delivered (Auto-filled)
    delivery_date = models.DateField(null=True, default=datetime.today()+timedelta(days=1))

    # Check if order is complete
    complete = models.BooleanField(default=False, null=True, blank=False)

    notes = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.order_date} - Total of PHP {self.total} (Convenience Fee: PHP {self.fees}"

    def delivery_date(self):
        return datetime.today()+timedelta(days=3)

class OrderInformation(models.Model):
    # User session id if user attribute does not exist (if user isn't logged in, use a session id instead)
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order = models.OneToOneField(
        Order, 
        related_name="order_information",
        null=True, 
        on_delete=models.SET_NULL
    )

    # Guest session user info
    session_sender = models.OneToOneField(
        CustomerInformation, 
        related_name="sender_information", 
        on_delete=models.SET_NULL, 
        null=True
    )
    
    # Guest session user address
    session_address = models.OneToOneField(
        Address, 
        related_name="sender_address", 
        on_delete=models.SET_NULL, 
        null=True
    )

    # Guest session user payment details
    session_payment = models.OneToOneField(
        BankAccount, 
        related_name="sender_address", 
        on_delete=models.SET_NULL, 
        null=True
    )

    # Guest session user payment details
    session_notifications = models.OneToOneField(
        Notification, 
        related_name="sender_address", 
        on_delete=models.SET_NULL, 
        null=True,
    )

    # JWT token ID
    token_jwt_id = models.CharField(max_length=999, null=True, blank=True)
    
    # For encoding token to jwt
    token_private_key = models.CharField(max_length=255, null=True, blank=True)

    # For decoding token to jwt
    token_public_key = models.CharField(max_length=255, null=True, blank=True)

    # JWT customer ID (eWallet)
    customer_jwt_id = models.CharField(max_length=999, null=True, blank=True)
    customer_private_key = models.CharField(max_length=255, null=True, blank=True)
    customer_public_key = models.CharField(max_length=255, null=True, blank=True)

class ProductOrder(models.Model):
    # Order cart
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL) 

    # Product ordered
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

    # Product size
    size = models.ForeignKey(Size, null=True, on_delete=models.SET_NULL)
    
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