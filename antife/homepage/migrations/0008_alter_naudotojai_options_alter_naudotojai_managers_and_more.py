# Generated by Django 5.0.2 on 2024-03-20 17:04

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('homepage', '0007_rename_usename_naudotojai_username'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='naudotojai',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='naudotojai',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='naudotojai',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AddField(
            model_name='naudotojai',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AddField(
            model_name='naudotojai',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterModelOptions(
            name='naudotojai',
            options={'verbose_name': 'lolname', 'verbose_name_plural': 'lolnames'},
        ),
        migrations.AlterModelOptions(
            name='naudotojai',
            options={'verbose_name': 'puuid', 'verbose_name_plural': 'puuids'},
        ),
        migrations.AlterModelOptions(
            name='naudotojai',
            options={'verbose_name': 'tier', 'verbose_name_plural': 'tiers'},
        ),
        migrations.AlterModelOptions(
            name='naudotojai',
            options={'verbose_name': 'rank', 'verbose_name_plural': 'ranks'},
        ),
        migrations.AddField(
            model_name='naudotojai',
            name='groups',
            field=models.ManyToManyField(related_name='naudotojai_groups', to='auth.group'),
        ),
        migrations.AddField(
            model_name='naudotojai',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AddField(
            model_name='naudotojai',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
        migrations.AddField(
            model_name='naudotojai',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='naudotojai',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AddField(
            model_name='naudotojai',
            name='user_permissions',
            field=models.ManyToManyField(related_name='naudotojai_permissions', to='auth.permission'),
        ),
        migrations.AlterField(
            model_name='naudotojai',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='naudotojai',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
