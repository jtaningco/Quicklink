# Generated by Django 3.0.6 on 2021-01-10 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_auto_20210111_0431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.CharField(choices=[('Made to Order', 'Made to Order'), ('1', '1'), ('2', '2'), ('3', '3')], default=('Made to Order', 'Made to Order'), max_length=55, null=True),
        ),
    ]
