from django.shortcuts import render, redirect
from homepage.models import Naudotojai, Team
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404

@login_required
def openCreateForm(request):
    # Check if the user already has a team
    if Team.objects.filter(fk_Naudotojasid_Naudotojas__user=request.user).exists():
        messages.error(request, 'You can only be a part of one team')
        return redirect('teams:komandaview')

    if request.method == 'POST':
        pavadinimas = request.POST.get('pavadinimas')
        if not pavadinimas:
            messages.error(request, 'Team title must be filled')
            return redirect('teams:create_komanda')

        naudotojai_instance = Naudotojai.objects.get(user=request.user)

        # Get all teams
        all_teams = GetAllTeams()

        # Check if the team name already exists
        existing_team_names = [team.pavadinimas for team in all_teams]
        if pavadinimas in existing_team_names:
            # If a team with the same name already exists, show an error message
            messages.error(request, 'Team title is already taken')
        else:
            # If the user doesn't have a team and a team with the same name doesn't exist, create a new team
            Team.objects.create(pavadinimas=pavadinimas, fk_Naudotojasid_Naudotojas=naudotojai_instance)
            # Add success message
            messages.success(request, 'Team was successfully created')
            # Redirect to the 'teamsview' view after creating the team
            return redirect('teams:teamsview')

    # If the request method is not POST or if there was an error, render the 'teamsview' template
    return openteams(request)



@login_required
def create_team_form(request):
    return render(request, 'CreateTeamForm.html')




def GetAllTeams():
    return Team.objects.all()

@login_required
def openteams(request):
    # Get all teams from the database using the separate function
    all_teams = GetAllTeams()

    # Get the team of the currently logged-in user
    user_team = Team.objects.filter(fk_Naudotojasid_Naudotojas__user=request.user).first()

    return render(request, 'TeamsView.html', {'all_teams': all_teams, 'user_team': user_team})


@login_required
def view_team(request, team_id):
    # Retrieve the team object using the team_id
    team = get_object_or_404(Team, id=team_id)

    # Pass the team object to the template
    return render(request, 'TeamInformationForm.html', {'team': team})

@login_required
def deleteTeam(request, team_id):
    try:
        team = Team.objects.get(pk=team_id)
        if team.fk_Naudotojasid_Naudotojas.user != request.user:
            messages.error(request, 'Jūs neturite teisės trinti šios komandos.')
            return redirect('teams:komandaview')
    except Team.DoesNotExist:
        messages.error(request, 'Komanda nerasta.')
        return redirect('teams:komandaview')

    # Call the checkConfirmation function to handle the confirmation check
    if checkConfirmation(request):
        team.delete()
        messages.success(request, 'Komanda buvo sėkmingai ištrinta.')
        return redirect('teams:teamsview')

    return render(request, 'ConfirmationView.html', {'team': team})

@login_required
def checkConfirmation(request):
    if request.method == 'POST' and 'confirmation' in request.POST:
        return True
    return False




@login_required
def openEditForm(request, team_id):
    # Retrieve the team object using the team_id
    team = get_object_or_404(Team, pk=team_id)
    
    # Check if the user has permission to edit this team
    if team.fk_Naudotojasid_Naudotojas.user != request.user:
        messages.error(request, 'Jūs neturite teisės redaguoti šios komandos.')
        return redirect('teams:komandaview')
    
    if request.method == 'POST':
        # If the form is submitted, update the team data with the new values
        new_pavadinimas = request.POST.get('pavadinimas')
        if new_pavadinimas:
            # Check if the new team name is already taken
            if Team.objects.exclude(pk=team_id).filter(pavadinimas=new_pavadinimas).exists():
                messages.error(request, 'Team titel is already taken')
            else:
                team.pavadinimas = new_pavadinimas
                team.save()
                messages.success(request, 'Team title was succesfully updated')
                return redirect('teams:teamsview')
        else:
            messages.error(request, 'Team title must be filled')
    
    # If the request method is GET or if there was an error, render the edit_team.html template with the team data
    return render(request, 'EditTeamForm.html', {'team': team})



