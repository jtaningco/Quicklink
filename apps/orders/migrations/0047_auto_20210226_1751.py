# Generated by Django 3.0.6 on 2021-02-26 17:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0046_auto_20210226_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 1, 17, 51, 16, 562493), null=True),
        ),
    ]
