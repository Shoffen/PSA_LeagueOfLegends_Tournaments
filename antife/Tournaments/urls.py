from django.urls import path
from .Controllers.User import TournamentController

app_name = 'tournaments'

urlpatterns = [
    path('', TournamentController.openTournaments, name='tournamentsview'),
    path('create_tournament/', TournamentController.createTournament, name='create_tournament'),
    path('edit_tournament/<int:tournament_id>/', TournamentController.editTournament, name='edit_tournament'),
    path('view_tournament/<int:tournament_id>/', TournamentController.viewTournament, name='view_tournament'),
    path('register_tournament/<int:tournament_id>/', TournamentController.register, name='register_tournament'),
    path('register-choose/<int:tournament_id>/',TournamentController.openRegisterChooseForm, name='register_choose_form'),
    path('register-solo/<int:tournament_id>/', TournamentController.openRegisterFormSolo, name='register_tournament_form_solo'),
    path('register-team/<int:tournament_id>/', TournamentController.openRegisterFormTeam, name='register_tournament_form_team'),
    path('score_board/<int:tournament_id>/', TournamentController.openScoreBoard, name='score_board'),

]
