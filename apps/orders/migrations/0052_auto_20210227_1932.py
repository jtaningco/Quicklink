# Generated by Django 3.0.6 on 2021-02-27 11:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0051_auto_20210227_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 2, 19, 32, 31, 443098), null=True),
        ),
    ]
