# Generated by Django 4.2.7 on 2024-04-17 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0015_valgomas_produktas_kiekis'),
    ]

    operations = [
        migrations.AddField(
            model_name='valgymo_receptas',
            name='kiekis',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
