# Generated by Django 3.0.6 on 2021-02-26 20:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0049_auto_20210226_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 1, 20, 20, 6, 524405), null=True),
        ),
    ]
