# Generated by Django 3.0.6 on 2021-02-10 13:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0028_auto_20210210_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 13, 21, 23, 3, 90232), null=True),
        ),
    ]
