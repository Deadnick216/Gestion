from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario  # Asegúrate de importar correctamente el modelo Usuario

class CustomUserCreationForm(UserCreationForm): 
    class Meta:
        model = Usuario
        fields = ('username', 'nombre', 'apellido', 'rol', 'bio')  # Incluye los nuevos campos
    
    # El campo username será el correo electrónico
    username = forms.EmailField(label="Correo electrónico")
    
    # Campos adicionales
    nombre = forms.CharField(label="Nombre", max_length=50, required=True)
    apellido = forms.CharField(label="Apellido", max_length=50, required=True)
    
    # Campo de rol, obligatorio y con un valor predeterminado
    rol = forms.ChoiceField(choices=Usuario.ROLES, initial='huesped', required=True)
    
    # Campos de contraseña
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput())
    
    # Campo opcional: biografía
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Biografía")

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre.strip():
            raise forms.ValidationError("El nombre no puede estar vacío.")
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if not apellido.strip():
            raise forms.ValidationError("El apellido no puede estar vacío.")
        return apellido
