from django.shortcuts import render, redirect
from homepage.models import Naudotojai, Team
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404



@login_required
def opentournaments(request):
    print("ateina")
    # Get all teams from the database using the separate function
    #all_teams = GetAllTeams()

    # Get the team of the currently logged-in user
    #user_team = Team.objects.filter(fk_Naudotojasid_Naudotojas__user=request.user).first()

    return render(request, 'TournamentsView.html')


