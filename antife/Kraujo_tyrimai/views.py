from django.shortcuts import render, redirect
from homepage.models import Kraujo_tyrimai, Naudotojai, Komanda
from django.contrib.auth.decorators import login_required
from .utils import get_plot
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
import datetime

@login_required
def create_komanda(request):
    # Check if the user already has a team
    if Komanda.objects.filter(fk_Naudotojasid_Naudotojas__user=request.user).exists():
        messages.error(request, 'Jūs jau turite komandą arba esate dalis komandos.')
        return redirect('kraujo_tyrimai:komandaview')

    if request.method == 'POST':
        pavadinimas = request.POST.get('pavadinimas')
        if not pavadinimas:
            messages.error(request, 'Pavadinimo laukas negali būti tuščias.')
            return redirect('kraujo_tyrimai:create_komanda')

        naudotojai_instance = Naudotojai.objects.get(user=request.user)

        existing_Team = Komanda.objects.filter(pavadinimas=pavadinimas).exists()
        if existing_Team:
            # If a team with the same name already exists, show an error message
            messages.error(request, 'Komandos pavadinimas užimtas')
        else:
            # If the user doesn't have a team and a team with the same name doesn't exist, create a new team
            Komanda.objects.create(pavadinimas=pavadinimas, fk_Naudotojasid_Naudotojas=naudotojai_instance)
            # Add success message
            messages.success(request, 'Komanda sėkmingai sukurta.')
            # Redirect to the 'komandaview' view after creating the team
            return redirect('kraujo_tyrimai:komandaview')

    # If the request method is not POST or if there was an error, render the 'komandaview' template
    return komandaview(request)






@login_required
def komandaview(request):
    # Get all teams from the database
    all_teams = Komanda.objects.all()

    # Get the team of the currently logged-in user
    user_team = Komanda.objects.filter(fk_Naudotojasid_Naudotojas__user=request.user).first()

    return render(request, 'Kraujotyr.html', {'all_teams': all_teams, 'user_team': user_team})

from django.shortcuts import render, get_object_or_404
from homepage.models import Komanda

def view_team(request, team_id):
    # Retrieve the team object using the team_id
    team = get_object_or_404(Komanda, id=team_id)

    # Pass the team object to the template
    return render(request, 'TeamView.html', {'team': team})

@login_required
def delete_team(request, team_id):
    try:
        team = Komanda.objects.get(pk=team_id)
        if team.fk_Naudotojasid_Naudotojas.user != request.user:
            messages.error(request, 'Jūs neturite teisės trinti šios komandos.')
            return redirect('kraujo_tyrimai:komandaview')
    except Komanda.DoesNotExist:
        messages.error(request, 'Komanda nerasta.')
        return redirect('kraujo_tyrimai:komandaview')

    if request.method == 'POST':
        team.delete()
        messages.success(request, 'Komanda sėkmingai ištrinta.')
        return redirect('kraujo_tyrimai:komandaview')

    return render(request, 'confirm_delete_team.html', {'team': team})







