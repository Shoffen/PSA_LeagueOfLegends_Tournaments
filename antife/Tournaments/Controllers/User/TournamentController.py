from django.shortcuts import render, redirect
from homepage.models import Naudotojai, Tournament, Team, TournamentTeam
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

from antife.RiotAPI.helpers import get_player_statistics_in_match, get_summoner_info, get_match_ids



def getAllTournaments():
    return Tournament.objects.all()

@login_required
def openTournaments(request):

    allTournaments = getAllTournaments()
    return render(request, 'TournamentsView.html', {'all_tournaments': allTournaments})

@login_required
def createTournament(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        rankRequirement = request.POST.get('rankRequirement')
        
        if not title or not rankRequirement:
            messages.error(request, 'All fields are required.')
            return redirect('create_tournament')

        naudotojai_instance = Naudotojai.objects.get(user=request.user)
        
        Tournament.objects.create(title=title, rankRequirement=rankRequirement, fk_Naudotojasid_Naudotojas=naudotojai_instance)
        messages.success(request, 'Tournament was successfully created.')
        return redirect('tournaments:tournamentsview')  # Redirect to a view that lists tournaments
    
    return render(request, 'TournamentForm.html')


@login_required
def editTournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        rankRequirement = request.POST.get('rankRequirement')

        if title and rankRequirement:
            tournament.title = title
            tournament.rankRequirement = rankRequirement
            tournament.save()
            messages.success(request, 'Tournament was successfully updated.')
            return redirect('tournaments:tournamentsview')
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'EditTournamentForm.html', {'tournament': tournament})

@login_required
def viewTournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    return render(request, 'SingleTournamentView.html', {'tournament': tournament})

@login_required
def register(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    user = request.user.naudotojai
    if user in tournament.registered_users.all():
        messages.warning(request, 'You are already registered for this tournament.')
    else:
        tournament.registered_users.add(user)
        messages.success(request, 'You have successfully registered for the tournament.')
    return redirect('tournaments:tournamentsview')

@login_required
def registerTeam(request, tournament_id, users):
    tournament = Tournament.objects.get(pk=tournament_id)
    user = request.user.naudotojai
    if user in tournament.registered_users.all():
        messages.warning(request, 'You are already registered for this tournament.')
    else:
        tournament.registered_users.add(user)
        messages.success(request, 'You have successfully registered for the tournament.')
    return redirect('tournaments:tournamentsview')

# views.py
from django.shortcuts import render

@login_required
def openRegisterChooseForm(request, tournament_id):
    
    return render(request, 'RegisterTournamentChooseForm.html', {'tournament_id': tournament_id})

@login_required
def openRegisterFormSolo(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    if request.method == 'POST':
        naudotojas = Naudotojai.objects.get(user=request.user)
        if checkData(tournament.rankRequirement, naudotojas.tier):
            return register(request, tournament_id)
        else:
            messages.error(request, 'Rank is too low.')
            return redirect('tournaments:tournamentsview')
    # Logic for solo registration form
    return render(request, 'RegisterTournamentFormSolo.html', {'tournament': tournament})

def openRegisterFormTeam(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    naudotojas = Naudotojai.objects.get(user=request.user)
    team = Team.objects.filter(members=naudotojas).first()
    
    if not team:
        messages.error(request, 'You are not part of any team.')
        return redirect('tournaments:tournamentsview')

    if request.method == 'POST':
        selected_member_ids = request.POST.getlist('members')
        
        # Include the current user in the selected members
        selected_member_ids.append(str(naudotojas.id))

        if len(selected_member_ids) > 5:
            messages.error(request, 'You can select up to 4 additional members only.')
            return redirect('tournaments:register_form_team', tournament_id=tournament_id)

        selected_members = Naudotojai.objects.filter(id__in=selected_member_ids)
        all_members_valid = all(checkData(tournament.rankRequirement, member.tier) for member in selected_members)
        
        if all_members_valid:
            tournament_team = TournamentTeam.objects.create(fk_Naudotojasid_Naudotojas=naudotojas)
            tournament_team.users.add(*selected_members)
            tournament.registered_teams.add(tournament_team)
            messages.success(request, 'Your team has been successfully registered for the tournament.')
        else:
            messages.error(request, 'One or more selected members do not meet the rank requirement.')

        return redirect('tournaments:tournamentsview')

    team_members = team.members.exclude(id=naudotojas.id)  # Exclude current user
    return render(request, 'RegisterTournamentFormTeam.html', {'tournament': tournament, 'team_members': team_members})
    
def convertRank(rank_raw):
    convertedRank=None
    rank = rank_raw.upper()
    if rank == "UNRANKED":
        convertedRank = 0
    elif rank == "IRON":
        convertedRank = 1
    elif rank == "BRONZE":
        convertedRank = 2
    elif rank == "SILVER":
        convertedRank = 3
    elif rank == "GOLD":
        convertedRank = 4
    elif rank == "PLATINUM":
        convertedRank = 5
    elif rank == "EMERALD":
        convertedRank = 6
    elif rank == "DIAMOND":
        convertedRank = 7
    elif rank == "MASTER":
        convertedRank = 8
    elif rank == "GRANDMASTER":
        convertedRank = 9
    elif rank == "CHALLENGER":
        convertedRank = 10
    else:
        convertedRank = -1
    return convertedRank

def checkData(requiredRank, playerRank):
    if(convertRank(playerRank) >= convertRank(requiredRank)):
        return True
    else:
        return False
