from django.urls import path
from .Controllers.User import TournamentController

app_name = 'tournaments'

urlpatterns = [
    path('', TournamentController.opentournaments, name='tournamentsview'),
    
]
