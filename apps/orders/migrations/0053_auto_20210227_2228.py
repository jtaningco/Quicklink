# Generated by Django 3.0.6 on 2021-02-27 14:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0052_auto_20210227_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 2, 22, 28, 12, 35285), null=True),
        ),
    ]