# Generated by Django 3.0.6 on 2021-03-04 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0060_productorder_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='fees',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, null=True),
        ),
    ]
