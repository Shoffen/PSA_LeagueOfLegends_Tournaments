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
import requests
from django.urls import reverse
from datetime import datetime
from django.shortcuts import render

from antife.RiotAPI.helpers import get_player_statistics_in_match, get_summoner_info, get_match_ids



def getAllTournaments():
    return Tournament.objects.all()

def getTeam(team_id):
    team = get_object_or_404(Team, id=team_id)
    return team


def getAllTournamentTeams(tournament_id):
    
    tournament = get_object_or_404(Tournament, id=tournament_id)
    tournament_teams = tournament.registered_teams.all()
    teams = []
    for team in tournament_teams:
        teams.append(getTeam(team.id))
    return teams

def findTeams(teams, count):
    cTeams = []
    for team in teams:
        if team.members.count() == count:
            cTeams.append(team)
    return cTeams
    

def removeFromWaiting(teams):
    teams.remove(0)
    return teams


def makeScoreBoard(tournament_id):
    teams = getAllTournamentTeams(tournament_id=tournament_id)
    
    approved_teams = []  
    teams_of_two = findTeams(teams, 2)
    teams_of_one = findTeams(teams, 1)
    teams_of_three = findTeams(teams, 3)
    teams_of_four = findTeams(teams, 4)

    for team in teams:
        if team.members.count() == 5:
            approved_teams.append(team)
        
        if team.members.count() == 3 and teams_of_two:
            team.members.add(*teams_of_two[0].members.all())
            print(teams_of_two[0].id)
            teams_of_two = teams_of_two[1:]
            removeFromWaiting(teams_of_two)
            approved_teams.append(team)

        if team.members.count() == 4 and teams_of_one:
            team.members.add(*teams_of_one[0].members.all())
            teams_of_one = teams_of_one[1:]
            removeFromWaiting(teams_of_one[0].id)
            approved_teams.append(team)
        

        if team.members.count() == 3 and len(teams_of_one) > 1:
            team.members.add(*teams_of_one[0].members.all())
            team.members.add(*teams_of_one[1].members.all())
            removeFromWaiting(teams_of_one[0].id)
            removeFromWaiting(teams_of_one[1].id)
            teams_of_one = teams_of_one[2:] 
            approved_teams.append(team)
        
        if team.members.count() == 2 and teams_of_two and teams_of_one:
            team.members.add(*teams_of_one[0].members.all())
            team.members.add(*teams_of_two[0].members.all())
            removeFromWaiting(teams_of_one[0].id)
            removeFromWaiting(teams_of_two[0].id)
            teams_of_one = teams_of_one[1:]  
            teams_of_two = teams_of_two[1:] 
            approved_teams.append(team)
    
    return approved_teams
        


@login_required
def openTournaments(request):
    all_tournaments = Tournament.objects.all()
    
    for tournament in all_tournaments:
        participant_count = tournament.registered_users.count()
        
        for team in tournament.registered_teams.all():
            participant_count += team.users.count()
        
        tournament.participant_count = participant_count

    return render(request, 'TournamentsView.html', {'all_tournaments': all_tournaments})

@login_required
def createTournament(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        rankRequirement = request.POST.get('rankRequirement')
        max_participants = request.POST.get('max_participants')

        if not title or not rankRequirement:
            messages.error(request, 'All fields are required.')
            return redirect('create_tournament')

        naudotojai_instance = Naudotojai.objects.get(user=request.user)
        
        Tournament.objects.create(title=title, rankRequirement=rankRequirement, fk_Naudotojasid_Naudotojas=naudotojai_instance, max_participants=max_participants)
        messages.success(request, 'Tournament was successfully created.')
        return redirect('tournaments:tournamentsview')  # Redirect to a view that lists tournaments
    
    return render(request, 'TournamentForm.html')


@login_required
def editTournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        rankRequirement = request.POST.get('rankRequirement')
        max_participants = request.POST.get('max_participants')

        if title and rankRequirement:
            tournament.title = title
            tournament.rankRequirement = rankRequirement
            tournament.max_participants = max_participants
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
    elif participant_count(tournament_id) > tournament.max_participants:
        messages.warning(request, 'Tournament is full')
    else:
        tournament.registered_users.add(user)
        messages.success(request, 'You have successfully registered for the tournament.')
    return redirect('tournaments:tournamentsview')

def participant_count(tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    total = tournament.registered_users.count()

    for team in tournament.registered_teams.all():
        total += team.users.count()
<<<<<<< Updated upstream

=======
    
>>>>>>> Stashed changes
    return total

# views.py
from django.shortcuts import render

@login_required
def openRegisterChooseForm(request, tournament_id):
    
    return render(request, 'RegisterTournamentChooseForm.html', {'tournament_id': tournament_id})

@login_required
def openScoreBoard(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    tournament_teams = makeScoreBoard(tournament_id)
    
    return render(request, 'ScoreBoardForm.html', {'tournament': tournament, 'tournament_teams': tournament_teams})

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
<<<<<<< Updated upstream
        if (selected_members.count()) >= tournament.max_participants:
=======
        
        if (participant_count(tournament_id) + selected_members.count()) > tournament.max_participants:
>>>>>>> Stashed changes
            messages.error(request, 'Tournament is too full.')
        elif all_members_valid:
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
