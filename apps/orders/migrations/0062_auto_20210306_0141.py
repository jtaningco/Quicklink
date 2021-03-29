# Generated by Django 3.0.6 on 2021-03-05 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0061_order_fees'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True),
        ),
    ]