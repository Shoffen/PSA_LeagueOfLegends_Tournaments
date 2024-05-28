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


def profilisview(request):
    user_id = None
    username = None
    vardas = None
    matches = []
    pavarde = None
    telefonas = None
    gimimo_Data = None
    el_pastas = None
    password = None
    form_submitted = False  # Initialize form_submitted to False

    if request.user.is_authenticated:
        user_id = request.user.id
        username = request.user.username
        el_pastas = request.user.email
        password = request.user.password
        try:
            # Retrieve the latest data from the database
            naudotojas = Naudotojai.objects.get(user=request.user)
            vardas = naudotojas.vardas
            pavarde = naudotojas.pavarde
            telefonas = naudotojas.telefonas
            gimimo_Data = naudotojas.gimimo_data
            tier = naudotojas.tier
            rank = naudotojas.rank

            summoner = get_summoner_info(naudotojas.lolname, "EUNE")

            # gets match ids, count default value 5
            match_ids = get_match_ids(naudotojas.lolname, "EUNE", 5)  # Get 5 match IDs

            for match_id in match_ids:
                player_statistics = get_player_statistics_in_match(match_id, naudotojas.puuid)
                matches.append(player_statistics)

            first_entry = summoner[0]
            LP = first_entry.get('leaguePoints', '0')
            wins = first_entry.get('wins', '0')
            loses = first_entry.get('loses', '0')

        except Naudotojai.DoesNotExist:
            # Handle the case where there's no related Naudotojai instance for the current user
            pass
    formatted_gimimo_Data = formats.date_format(gimimo_Data, "Y-m-d") if gimimo_Data else ""
    context = {
        'user_id': user_id,
        'match1': matches[0],
        'match2': matches[1],
        'match3': matches[2],
        'match4': matches[3],
        'match5': matches[4],
        'LP': LP,
        'wins': wins,
        'losses': loses,
        'tier': tier,
        'rank': rank,
        'username': username,
        'password': password,
        'vardas': vardas,
        'pavarde': pavarde,
        'telefonas': telefonas,
        'gimimo_Data': formatted_gimimo_Data,
        'el_pastas': el_pastas,
        'form_submitted': form_submitted,  # Pass form_submitted to the template
    }
    
    # Clear any existing messages
    storage = messages.get_messages(request)
    storage.used = True

    return render(request, 'Profilis.html', context)


from django.contrib import messages

def save_profile_changes(request):
    if request.method == 'POST':
        # Retrieve form data from the request
        username = request.POST.get('username')
        vardas = request.POST.get('vardas')
        pavarde = request.POST.get('pavarde')
        telefonas = request.POST.get('telefonas')
        gimimo_data = request.POST.get('birthday')  # Get the date string from the form
        el_pastas = request.POST.get('el_pastas')

        # Retrieve the user's profile from the database
        naudotojas = Naudotojai.objects.get(user=request.user)

        error_messages = []  # Initialize a list to store error messages

        # Update the user's email
        if el_pastas:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", el_pastas) or not el_pastas.endswith('@gmail.com'):
                error_messages.append('Neteisingai įvestas elektronins paštas. Įveskite teisingą naudodami @gmail.com')
            else:
                request.user.email = el_pastas
                request.user.save()

        # Validate and update other fields
        if gimimo_data:
            try:
                birthdate_obj = datetime.strptime(gimimo_data, '%Y-%m-%d').date()
                today = datetime.now().date()
                if birthdate_obj >= today:
                    raise ValueError  # Birthdate should be in the past
            except ValueError:
                error_messages.append('Neteisinga gimimo data. Pasirinkite dar kartą.')
            else:
                naudotojas.gimimo_data = gimimo_data

        if vardas:
            naudotojas.vardas = vardas
        if pavarde:
            naudotojas.pavarde = pavarde
        if telefonas:
            if not re.match(r"\+370\d{8}$", telefonas):
                error_messages.append('Neteisingai įvestas telefono numeris.  Įveskite iš naujo naudodami prefiksą +370')
            else:
                naudotojas.telefonas = telefonas
        if el_pastas:
            naudotojas.el_pastas = el_pastas
        if username:
            if User.objects.filter(username=username).exclude(pk=request.user.pk).exists():
                error_messages.append('Šis slapyvardis jau užimtas')
            else:
                request.user.username = username
                request.user.save()

        # Save the updated profile if there are no error messages
        if not error_messages:
            try:
                naudotojas.save()
                messages.success(request, 'Profilis sėkmingai atnaujintas')
                # Redirect the user to the profile page or any other page as needed
                return redirect('profilis:profilisview')
            except Exception as e:
                error_messages.append(f'Klaida atnaujinant profilį: {str(e)}')

        # If there are error messages, add them to the messages framework
        for message in error_messages:
            messages.error(request, message)

        # Redirect back to the editing page with error messages
        return redirect(reverse('profilis:profilisview'))

def user_list(request):
    users = User.objects.all()
    return render(request, 'UsersView.html', {'users': users})

def user_profile_view(request, user_id):
    user_n = User.objects.get(id=user_id)
    user_id = user_id
    username = None
    vardas = None
    matches = []
    pavarde = None
    telefonas = None
    gimimo_Data = None
    el_pastas = None
    password = None
    form_submitted = False  # Initialize form_submitted to False

    if user_n.is_authenticated:
        username = user_n.username
        el_pastas = user_n.email
        password = user_n.password
        try:
            # Retrieve the latest data from the database
            naudotojas = Naudotojai.objects.get(user=user_n)
            vardas = naudotojas.vardas
            pavarde = naudotojas.pavarde
            telefonas = naudotojas.telefonas
            gimimo_Data = naudotojas.gimimo_data
            tier = naudotojas.tier
            rank = naudotojas.rank
            

            summoner = get_summoner_info(naudotojas.lolname, "EUNE")

            # gets match ids, count default value 5
            match_ids = get_match_ids(naudotojas.lolname, "EUNE", 5)  # Get 5 match IDs

            for match_id in match_ids:
                player_statistics = get_player_statistics_in_match(match_id, naudotojas.puuid)
                matches.append(player_statistics)

            first_entry = summoner[0]
            LP = first_entry.get('leaguePoints', '0')
            wins = first_entry.get('wins', '0')
            loses = first_entry.get('loses', '0')

        except Naudotojai.DoesNotExist:
            # Handle the case where there's no related Naudotojai instance for the current user
            pass
    formatted_gimimo_Data = formats.date_format(gimimo_Data, "Y-m-d") if gimimo_Data else ""
    context = {
        'user_id': user_id,
        'match1': matches[0],
        'match2': matches[1],
        'match3': matches[2],
        'match4': matches[3],
        'match5': matches[4],
        'LP': LP,
        'wins': wins,
        'losses': loses,
        'tier': tier,
        'rank': rank,
        'username': username,
        'password': password,
        'vardas': vardas,
        'pavarde': pavarde,
        'telefonas': telefonas,
        'gimimo_Data': formatted_gimimo_Data,
        'el_pastas': el_pastas,
        'form_submitted': form_submitted,
        'show_report_button': True,  # Pass form_submitted to the template
    }
    
    # Clear any existing messages
    storage = messages.get_messages(request)
    storage.used = True
    return render(request, 'Profilis.html', context)
