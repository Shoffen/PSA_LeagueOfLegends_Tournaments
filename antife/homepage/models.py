from django.db import models
from django.contrib.auth.models import User

class Naudotojai(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    vardas = models.CharField(max_length=255)
    pavarde = models.CharField(max_length=255)
    telefonas = models.CharField(max_length=255)
    el_pastas = models.CharField(max_length=255)
    gimimo_data = models.DateField()
    level = models.IntegerField()
    last_login = models.DateTimeField(null=True, blank=True)

