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
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    apellido = models.CharField(max_length=50, verbose_name="Apellido")

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.username})"