# Generated by Django 3.0.6 on 2021-02-10 10:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0026_auto_20210210_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 13, 10, 38, 36, 302736), null=True),
        ),
    ]
