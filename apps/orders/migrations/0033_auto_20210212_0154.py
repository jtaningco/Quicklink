# Generated by Django 3.0.6 on 2021-02-11 17:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0032_auto_20210210_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 15, 1, 54, 51, 496380), null=True),
        ),
    ]
