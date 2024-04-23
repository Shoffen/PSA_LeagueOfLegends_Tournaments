from django.urls import path
from . import views
from .views import create_komandos

app_name = 'komandos'

urlpatterns = [
    path('', views.komandaview, name='komandaview'),
    path('create_komandos/', create_komandos, name='create_komandos'),
]