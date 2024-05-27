from django.shortcuts import render, redirect, get_object_or_404
from homepage.models import Naudotojai, Tournament, Team, TournamentTeam, Messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django import forms
from homepage.models import Naudotojai
from django.utils import formats
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
import re
from django.urls import reverse
from datetime import datetime
from django.shortcuts import render
from django.contrib import messages as django_messages
from antife.RiotAPI.helpers import get_player_statistics_in_match, get_summoner_info, get_match_ids

@login_required
def admin_reports_view(request):
    reports = Messages.objects.all()
    return render(request, 'AllReports.html', {'reports': reports})

@login_required
def view_report(request, report_id):
    report = get_object_or_404(Messages, id=report_id)
    return render(request, 'ReportsView.html', {'report': report})

@login_required
def send_report_message(request, reported_profile_id):
    if request.method == 'POST':
        message_text = request.POST.get('message_text', '')

        if message_text.strip() == '':
            django_messages.error(request, 'Message text cannot be empty.')
            return redirect('send_message', {'reported_profile_id': reported_profile_id})

        reported_profile = Naudotojai.objects.get(id=reported_profile_id)

        # Assuming the current user is the reporter
        reporter = request.user

        # Create and save the message
        report_message = Messages.objects.create(reporter=reporter, reported_profile=reported_profile, message_text=message_text)
        report_message.save()

        django_messages.success(request, 'Report message sent successfully.')
        return render(request, 'MessageForm.html')

    else:
        django_messages.error(request, 'Invalid request method.')
        return redirect('send_message', {'reported_profile_id': reported_profile_id})

@login_required
def mark_report_handled(request, report_id):
    report = get_object_or_404(Messages, id=report_id)
    report.action_taken = True
    report.action_text = "Handled by admin"
    report.save()
    return redirect('admin_reports_view')

@login_required
def ban_user(request, user_id, report_id):
    user = get_object_or_404(Naudotojai, id=user_id)
    user.is_banned = True
    user.save()
    messages.success(request, f'User {user.username} has been banned.')
    mark_report_handled(report_id)
    return redirect('admin_reports_view')