from django.urls import path, include
from .views import home, login, register, logout_view, loged

urlpatterns = [
   path("", home, name="home"),
   path('login/', login, name='login'),
   path('register/', register, name='register'),
   path('logout/', logout_view, name='logout'),
   path('mityba/', include('Mityba.urls', namespace='mityba')),
   path('forumas/', include('Forumas.urls', namespace='forumas')),
   path('profilis/', include('Profilis.urls', namespace='profilis')), 
   path('teams/', include('Teams.urls', namespace='teams')), 
   path('tournaments/', include('Tournaments.urls', namespace='tournaments')),
   path('baseLogged/', loged, name='loged'),
   path('auth/', include('Authentication.urls', namespace='authentication')),
]
