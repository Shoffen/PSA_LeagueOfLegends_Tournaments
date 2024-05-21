from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from antife.RiotAPI.helpers import get_account_by_riot_id, get_summoner_info, get_summoner_ids
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login

def openRegisterForm(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'RegisterForm.html', {'form': form})

# authentication/Controllers/UserController.py

from django.shortcuts import render, redirect
from django.contrib import messages
from homepage.models import Naudotojai  # Assuming you have a User model defined in models.py
import re

from datetime import datetime
from django.http import HttpResponse  # Import HttpResponse

def submitData(request):
    if request.method == 'POST':
        # Retrieve form data
        email = request.POST.get('email')
        username = request.POST.get('username')
        name = request.POST.get('name')
        lolname = request.POST.get('lolname')
        lastName = request.POST.get('lastName')
        phoneNumber = request.POST.get('phoneNumber')
        birthday = request.POST.get('birthday')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        
        # Create a dictionary containing the form data
        form_data = {
            'email': email,
            'username': username,
            'name': name,
            'lolname': lolname,
            'lastName': lastName,
            'phoneNumber': phoneNumber,
            'birthday': birthday,
            'password': password,
            'repeat_password': repeat_password,
        }
        
        # Pass the form data to the checkValidation function
        return checkRegisterValidation(form_data, request)



def getAll():
    return Naudotojai.objects.all()

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.contrib import messages
from datetime import datetime
import re

def checkRegisterValidation(data, request):
    # Extract form data
    email = data.get('email')
    username = data.get('username')
    name = data.get('name')
    lolname = data.get('lolname')
    lastName = data.get('lastName')
    phoneNumber = data.get('phoneNumber')
    birthday = data.get('birthday')
    password = data.get('password')
    repeat_password = data.get('repeat_password')
    
    # Perform validation checks
    if User.objects.filter(username=username).exists():
        messages.error(request, 'Šis slapyvardis jau užimtas!')
        return render(request, 'register.html')
        
    # Validate email format using regular expression
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email) or not email.endswith('@gmail.com'):
        messages.error(request, 'Neteisingai įvestas elektronins paštas. Įveskite teisingą.')
        return render(request, 'register.html')
        
    elif User.objects.filter(email=email).exists():
        messages.error(request, 'Šis elektroninis paštas jau užimtas.')
        return render(request, 'register.html')
        
    elif not re.match(r"\+370\d{8}", phoneNumber):
        messages.error(request, 'Neteisingai įvestas telefono numeris. Įveskite per naują')
        return render(request, 'register.html')
        
    else:
        # Validate birthdate format and range
        try:
            birthdate_obj = datetime.strptime(birthday, '%Y-%m-%d').date()
            today = datetime.now().date()
            if birthdate_obj >= today:
                raise ValueError  # Birthdate should be in the past
        except ValueError:
            messages.error(request, 'Neteisinga gimimo data. Pasirinkite dar kartą.')
            return render(request, 'register.html')

        try:
            with transaction.atomic():
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Hash the password
                hashed_password = make_password(password)

                # get puuid
                puuid = None

                try:
                    puuid = get_account_by_riot_id(lolname, "EUNE")['puuid']
                    summoner = get_summoner_info(lolname, "EUNE")
                    print("Summoner Data:", summoner)  # Debug print to see the summoner object

                    if not summoner:
                        raise ValueError('Summoner not found or API request failed.')

                    first_entry = summoner[0]
                    tier = first_entry.get('tier', 'unranked')
                    rank = first_entry.get('rank', 'unranked')
                    # Do something with tier and rank

                except (IndexError, ValueError, KeyError, TypeError) as e:
                    messages.error(request, 'Neegzistuoja toks League of Legends zaidejas.')
                    return render(request, 'register.html')

                # Save the user profile data to the database
                new_user_profile = Naudotojai(
                    user=user,  # Associate the profile with the newly created user
                    lolname=lolname,
                    puuid=puuid,
                    tier=tier,
                    rank=rank,
                    vardas=name,
                    telefonas=phoneNumber,
                    pavarde=lastName,
                    gimimo_data=birthdate_obj,
                    level=0  # Set default level or adjust as needed
                )
                new_user_profile.save()

                sendEmail(email)

        except IntegrityError:
            messages.error(request, 'An error occurred while creating your account. Please try again.')
            return render(request, 'register.html')

        messages.success(request, 'Registracija sėkminga. Gali bandyt prisijungt!')
        return redirectToLogin()

def redirectToLogin():
    return redirect('/login')


def redirectToLogin():
    return redirect('/login')
    
def sendEmail(email):
    # Email credentials
        #emailSender = 'vartvald2023@outlook.com'
        #passwordd = 'xwe449#123!@'

        emailSender = 'lolsistema2024@outlook.com'
        passwordd = 'qrtyjgsjjug#$789'

        # SMTP server configuration
        smtp_server = 'smtp-mail.outlook.com'
        smtp_port = 587

        # Create message container
        msg = MIMEMultipart()
        msg['From'] = emailSender
        msg['To'] = email  # Replace with the recipient's email
        msg['Subject'] = 'Nauja paskyra užregistruota.'

        # Message body
        body = """"\
            <p>Sveiki,</p>
            <p>Nauja paskyra buvo sėkmingai užregistruota.</p>"""

        msg.attach(MIMEText(body, 'html'))

        # Connect to SMTP server and send email
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(emailSender, passwordd)
            server.send_message(msg)
            server.quit()
            print('Message sent successfully')
        except Exception as e:
            print('Message sending failed:', e)

def openLoginWindow(request):

    return render(request, 'UserLoginForm.html')

def submitLoginData(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        form_data = {
            'username': username,
            'password': password,
        }
    return checkData(form_data, request)

def checkData(data, request):
    username =data.get('username')
    password = data.get('password')
    
    Naudotojai = getAll()
    #Naudotojai.using.__annotations__ = user

    user = authenticate(request, username=username, password=password)

    if user is not None and user.is_active:
        django_login(request, user)
        messages.success(request, f"Login was succesfull! Welcome, {username}")
        if determineAccountType(user):
            return render(request, 'AdminHomePageForm.html')  # Redirect to the main forum page
        else:
             return render(request, 'userHomePageForm.html')  # Redirect to the main forum page
    else:
        messages.error(request, "Incorrect login data. Try again.")

    return render(request, 'UserLoginForm.html')

def determineAccountType(user):
    return user.is_staff

from django.contrib.auth import logout

def logOut(request):

    logout(request)
    
    return (flushSession(request)) 
 
def flushSession(request):
    request.session.flush() # Clear all session data
    return render(request, 'home.html')

def changePassword(request):
        return render (request, 'home.html')