# Generated by Django 3.1.3 on 2021-03-18 14:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0073_order_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(default=datetime.datetime(2021, 3, 19, 22, 15, 37, 359270), null=True),
        ),
    ]