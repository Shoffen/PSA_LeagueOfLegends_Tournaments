from django.urls import path
from Profilis.Controllers import UserController

app_name = 'profilis'

urlpatterns = [
    path('', UserController.OpenProfileView, name='profilisview'),
    path('save_profile_changes/', UserController.save_profile_changes, name='save_profile_changes'),
    path('profilis/', UserController.OpenProfileView, name='profilis'),
]
