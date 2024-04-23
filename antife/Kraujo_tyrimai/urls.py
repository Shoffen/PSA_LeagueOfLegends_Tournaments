from django.urls import path
from . import views
from .views import create_komanda

app_name = 'kraujo_tyrimai'

urlpatterns = [
    path('', views.komandaview, name='komandaview'),
    path('create_komanda/', create_komanda, name='create_komanda'),
    path('view_team/<int:team_id>/', views.view_team, name='view_team'),
    path('delete_team/<int:team_id>/', views.delete_team, name='delete_team'),
    
]