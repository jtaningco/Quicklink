# Generated by Django 3.0.6 on 2021-02-11 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20210212_0154'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerinformation',
            old_name='customer_mobile_number',
            new_name='customer_contact_number',
        ),
    ]
