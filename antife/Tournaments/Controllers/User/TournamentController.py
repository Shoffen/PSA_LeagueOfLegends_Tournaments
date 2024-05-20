from django.shortcuts import render, redirect
from homepage.models import Naudotojai, Tournament
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404





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
    return redirect('tournaments:view_tournament', tournament_id=tournament_id)

# views.py
from django.shortcuts import render

def openRegisterChooseForm(request, tournament_id):
    return render(request, 'RegisterTournamentChooseForm.html', {'tournament_id': tournament_id})

def openRegisterFormSolo(request, tournament_id):
    # Logic for solo registration form
    return render(request, 'RegisterTournamentFormSolo.html', {'tournament_id': tournament_id})

def openRegisterFormTeam(request, tournament_id):
    # Logic for team registration form
    return render(request, 'RegisterTournamentFormTeam.html', {'tournament_id': tournament_id})


