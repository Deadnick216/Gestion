from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuarios.models import Usuario

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'rol', 'bio')