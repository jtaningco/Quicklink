# Generated by Django 3.0.6 on 2021-01-09 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_auto_20210109_1806'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image_one',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image_three',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image_two',
        ),
        migrations.RemoveField(
            model_name='product',
            name='tags',
        ),
    ]
