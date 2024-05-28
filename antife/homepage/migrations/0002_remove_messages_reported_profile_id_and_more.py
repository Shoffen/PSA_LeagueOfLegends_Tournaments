# Generated by Django 5.0.6 on 2024-05-28 09:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='reported_profile_id',
        ),
        migrations.AddField(
            model_name='messages',
            name='reported_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_topic', to='homepage.naudotojai'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='reporter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_sender', to='homepage.naudotojai'),
        ),
    ]