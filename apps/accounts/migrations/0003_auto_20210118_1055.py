# Generated by Django 3.0.6 on 2021-01-18 02:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210107_1631'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='mobile_number',
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.CreateModel(
            name='PersonalInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('middle_initial', models.CharField(blank=True, default='', max_length=10, verbose_name='middle initial')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('mobile_number', models.CharField(max_length=15, null=True, verbose_name='mobile number')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='personal_information', to='accounts.User')),
            ],
        ),
    ]
