# Generated by Django 3.1.7 on 2021-03-25 10:12

import apps.accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20210324_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopdeliverysettings',
            name='city',
            field=models.CharField(blank=True, choices=[('Caloocan City', 'Caloocan'), ('Las Piñas City', 'Las Piñas'), ('Makati City', 'Makati'), ('Malabon City', 'Malabon'), ('Malanduyong City', 'Malanduyong'), ('Manila City', 'Manila'), ('Marikina City', 'Marikina'), ('Muntinlupa City', 'Muntinlupa'), ('Navotas City', 'Navotas'), ('Parañaque City', 'Parañaque'), ('Pasay City', 'Pasay'), ('Pasig City', 'Pasig'), ('Pateros City', 'Pateros'), ('Quezon City', 'Quezon City'), ('San Juan City', 'San Juan'), ('Taguig City', 'Taguig'), ('Valenzuela City', 'Valenzuela')], default=None, max_length=55, null=True, verbose_name='delivery city'),
        ),
        migrations.AlterField(
            model_name='shopdeliverysettings',
            name='line1',
            field=models.CharField(blank=True, default='', max_length=155, null=True, verbose_name='delivery line1'),
        ),
        migrations.AlterField(
            model_name='shopdeliverysettings',
            name='postal_code',
            field=models.CharField(blank=True, default='', max_length=4, null=True, validators=[apps.accounts.validators.only_int], verbose_name='delivery postal code'),
        ),
        migrations.AlterField(
            model_name='shopdeliverysettings',
            name='province',
            field=models.CharField(blank=True, choices=[('Metro Manila', 'Metro Manila')], default=None, max_length=55, null=True, verbose_name='delivery province'),
        ),
        migrations.AlterField(
            model_name='shopgeneralsettings',
            name='delivery_from_hour',
            field=models.PositiveSmallIntegerField(choices=[(0, '12:00 AM'), (1, '1:00 AM'), (2, '2:00 AM'), (3, '3:00 AM'), (4, '4:00 AM'), (5, '5:00 AM'), (6, '6:00 AM'), (7, '7:00 AM'), (8, '8:00 AM'), (9, '9:00 AM'), (10, '10:00 AM'), (11, '11:00 AM'), (12, '12:00 PM'), (13, '1:00 PM'), (14, '2:00 PM'), (15, '3:00 PM'), (16, '4:00 PM'), (17, '5:00 PM'), (18, '6:00 PM'), (19, '7:00 PM'), (20, '8:00 PM'), (21, '9:00 PM'), (22, '10:00 PM'), (23, '11:00 PM')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='shopgeneralsettings',
            name='delivery_to_hour',
            field=models.PositiveSmallIntegerField(choices=[(0, '12:00 AM'), (1, '1:00 AM'), (2, '2:00 AM'), (3, '3:00 AM'), (4, '4:00 AM'), (5, '5:00 AM'), (6, '6:00 AM'), (7, '7:00 AM'), (8, '8:00 AM'), (9, '9:00 AM'), (10, '10:00 AM'), (11, '11:00 AM'), (12, '12:00 PM'), (13, '1:00 PM'), (14, '2:00 PM'), (15, '3:00 PM'), (16, '4:00 PM'), (17, '5:00 PM'), (18, '6:00 PM'), (19, '7:00 PM'), (20, '8:00 PM'), (21, '9:00 PM'), (22, '10:00 PM'), (23, '11:00 PM')], default=None, null=True),
        ),
    ]