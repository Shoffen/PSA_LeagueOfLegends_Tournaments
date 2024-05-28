# Generated by Django 5.0.6 on 2024-05-27 17:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='max_participants',
            field=models.IntegerField(default=30),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='registered_users',
            field=models.ManyToManyField(related_name='registered_tournaments_solo', to='homepage.naudotojai'),
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_text', models.CharField(max_length=1000)),
                ('action_taken', models.BooleanField(default=False)),
                ('action_text', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reported_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_reports', to='homepage.naudotojai')),
                ('reporter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_reports', to='homepage.naudotojai')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fk_Naudotojasid_Naudotojas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.naudotojai')),
                ('users', models.ManyToManyField(related_name='registered_in_tournament_team', to='homepage.naudotojai')),
            ],
        ),
        migrations.AddField(
            model_name='tournament',
            name='registered_teams',
            field=models.ManyToManyField(related_name='registered_tournaments_teams', to='homepage.tournamentteam'),
        ),
    ]