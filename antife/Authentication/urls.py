from django.urls import path
from .Controllers.User import UserController  # Corrected import path

app_name = 'authentication'

urlpatterns = [
    path('register/', UserController.openRegisterForm, name='register'),
    path('submit/', UserController.submitData, name='submit_data'),  # Add this line
    path('login/', UserController.openLoginWindow, name='login'),
    path('submit_login/', UserController.submitLoginData, name='submit_login_data'),  # Add this line
    path('logout/', UserController.logOut, name='logout'),
    # Add other URL patterns as needed
]
