# Generated by Django 3.0.6 on 2021-02-10 14:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0031_auto_20210210_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 13, 22, 20, 2, 541079), null=True),
        ),
    ]