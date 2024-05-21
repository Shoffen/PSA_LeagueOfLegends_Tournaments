from django.shortcuts import render, redirect, get_object_or_404
from homepage.models import Naudotojai, Team
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def openCreateForm(request):

    create_team_form(request)

def submitData(request):
   
    if request.method == 'POST':
        pavadinimas = request.POST.get('pavadinimas')
        if not pavadinimas:
            messages.error(request, 'Team title must be filled')
            return redirect('teams:teamsview')

    return checkData(pavadinimas, request)
       

    
def checkData(pavadinimas, request):
    # Check if the user already has a team
    if Team.objects.filter(members=request.user.naudotojai).exists():
        messages.error(request, 'You can only be a part of one team')
        return redirect('teams:komandaview')
    naudotojai_instance = Naudotojai.objects.get(user=request.user)
    # Check if the team name already exists
    if Team.objects.filter(pavadinimas=pavadinimas).exists():
        messages.error(request, 'Team title is already taken')
    else:
        return createAs(pavadinimas, naudotojai_instance, request)
        
    
def createAs(pavadinimas, naudotojai_instance, request):
    team = Team.objects.create(pavadinimas=pavadinimas, fk_Naudotojasid_Naudotojas=naudotojai_instance)
    team.members.add(naudotojai_instance)
    messages.success(request, 'Team was successfully created')
    return redirect('teams:teamsview')

@login_required
def openCreateForm(request):
    return create_team_form(request)
   
@login_required
def create_team_form(request):
  
    return render(request, 'CreateTeamForm.html')

@login_required
def join_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    user = request.user.naudotojai
    
    # Check if the user is in any team
    user_teams = Team.objects.filter(members=user)
    if user_teams.exists() and not user_teams.filter(pk=team_id).exists():
        messages.error(request, 'You belong to another team and cannot join a new one.')
    elif user in team.members.all():
        messages.warning(request, 'You are already a member of this team.')
    else:
        team.members.add(user)
        messages.success(request, 'You have successfully joined the team.')
    
    return redirect('teams:view_team', team_id=team_id)

def checkRankRequirements(request, rank, requirement): 
    return rank == requirement
@login_required
def leave_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    user = request.user.naudotojai
    if user in team.members.all():
        team.members.remove(user)
        messages.success(request, 'You have successfully left the team.')
    else:
        messages.warning(request, 'You are not a member of this team.')
    return redirect('teams:view_team', team_id=team_id)

@login_required
def openteams(request):
    all_teams = GetAllTeams()
    user_team = Team.objects.filter(members=request.user.naudotojai).first()
    return render(request, 'TeamsView.html', {'all_teams': all_teams, 'user_team': user_team})

@login_required
def openTeamView(request, team_id):
    team = getTeam(team_id)
    return render(request, 'SingleTeamView.html', {'team': team})

def getTeam(team_id):
    return get_object_or_404(Team, id=team_id)

@login_required
def deleteTeam(request, team_id):
    try:
        team = Team.objects.get(pk=team_id)
        if team.fk_Naudotojasid_Naudotojas.user != request.user:
            messages.error(request, 'Jūs neturite teisės trinti šios komandos.')
            return redirect('teams:teamsview')
    except Team.DoesNotExist:
        messages.error(request, 'Komanda nerasta.')
        return redirect('teams:teamsview')

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
    team = get_object_or_404(Team, pk=team_id)
    
    if team.fk_Naudotojasid_Naudotojas.user != request.user:
        messages.error(request, 'Jūs neturite teisės redaguoti šios komandos.')
        return redirect('teams:view_team')
    
    if request.method == 'POST':
        new_pavadinimas = request.POST.get('pavadinimas')
        if new_pavadinimas:
            if Team.objects.exclude(pk=team_id).filter(pavadinimas=new_pavadinimas).exists():
                messages.error(request, 'Team title is already taken')
            else:
                team.pavadinimas = new_pavadinimas
                team.save()
                messages.success(request, 'Team title was successfully updated')
                return redirect('teams:teamsview')
        else:
            messages.error(request, 'Team title must be filled')
    
    return render(request, 'EditTeamForm.html', {'team': team})

def GetAllTeams():
    return Team.objects.all()
