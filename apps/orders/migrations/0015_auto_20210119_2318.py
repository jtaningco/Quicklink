# Generated by Django 3.0.6 on 2021-01-19 15:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_auto_20210118_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 22, 23, 18, 32, 233291), null=True),
        ),
    ]
