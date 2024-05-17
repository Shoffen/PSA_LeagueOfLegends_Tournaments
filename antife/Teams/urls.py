from django.urls import path
from .Controllers.User import TeamController
from .Controllers.User.TeamController import openCreateForm

app_name = 'teams'

urlpatterns = [
    path('', TeamController.openteams, name='teamsview'),
    path('create_team/', openCreateForm, name='create_team'),
    path('view_team/<int:team_id>/', TeamController.view_team, name='view_team'),
    path('delete_team/<int:team_id>/', TeamController.deleteTeam, name='delete_team'),
    path('edit_team/<int:team_id>/', TeamController.openEditForm, name='edit_team'),
    path('create-team/', TeamController.create_team_form, name='create_team_form'),
    path('join/<int:team_id>/', TeamController.join_team, name='join_team'),
    path('team/<int:team_id>/leave/', TeamController.leave_team, name='leave_team'),
]
