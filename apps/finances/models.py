from django.db import models

from apps.orders.models import Order

# Create your models here.
class Summary(models.Model):
    # Total Expected Revenue
    total_expected = models.DecimalField(null=True, default=0, max_digits=15, decimal_places=2)

    # Payments Received
    total_received = models.DecimalField(null=True, default=0, max_digits=15, decimal_places=2)

    # Accounts Receivables
    total_receivables = models.DecimalField(null=True, default=0, max_digits=15, decimal_places=2)