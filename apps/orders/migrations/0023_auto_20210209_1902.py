# Generated by Django 3.0.6 on 2021-02-09 19:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0022_auto_20210208_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 12, 19, 2, 14, 779258), null=True),
        ),
    ]