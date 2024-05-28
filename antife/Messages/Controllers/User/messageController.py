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
import logging
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
    reported_profile = get_object_or_404(Naudotojai, user_id=reported_profile_id)
    reporter = get_object_or_404(Naudotojai, user_id=request.user)
    if request.method == 'POST':
        print(reported_profile_id)
        message_text = request.POST.get('message_text')

        if not message_text:
            django_messages.error(request, 'Message text cannot be empty.')
        else:
            
            print("Reported id: " + str(reported_profile_id))
            # Create and save the message
            Messages.objects.create(reporter=reporter, reported_profile=reported_profile, message_text=message_text)

            messages.success(request, 'Report message sent successfully.')
            return redirect(reverse('profilis:view_profile', kwargs={'user_id': reported_profile_id}))

    return render(request, 'MessageForm.html', {'reported_profile_id': reported_profile_id})

@login_required
def mark_report_handled(request, report_id):
   
    return redirect('admin_reports_view')

@login_required
def ban_user(request, user_id, report_id):
    
    return redirect('admin_reports_view')