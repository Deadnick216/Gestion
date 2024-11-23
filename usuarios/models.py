from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    ROLES = [
        ('huesped', 'Huésped'),
        ('anfitrion', 'Anfitrión'),
        ('admin', 'Administrador'),
    ]
    rol = models.CharField(max_length=10, choices=ROLES, default='huesped')
    bio = models.TextField(blank=True, null=True)
