# Generated by Django 3.0.6 on 2021-02-26 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0033_auto_20210226_1841'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='week',
            new_name='schedule',
        ),
    ]
