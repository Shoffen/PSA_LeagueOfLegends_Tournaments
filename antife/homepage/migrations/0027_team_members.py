# Generated by Django 5.0.2 on 2024-05-17 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0026_rename_komanda_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name='teams_joined', to='homepage.naudotojai'),
        ),
    ]