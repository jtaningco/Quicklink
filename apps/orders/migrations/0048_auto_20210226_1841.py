# Generated by Django 3.0.6 on 2021-02-26 18:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0047_auto_20210226_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 1, 18, 41, 34, 420676), null=True),
        ),
    ]
