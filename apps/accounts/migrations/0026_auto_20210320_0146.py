# Generated by Django 3.1.7 on 2021-03-20 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20210319_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverydays',
            name='shop',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_days_shop', to='accounts.shopinformation'),
        ),
        migrations.AlterField(
            model_name='openhours',
            name='shop',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='open_hours_shop', to='accounts.shopinformation'),
        ),
    ]