from django.urls import path
from usuarios.views import home, register, login_view, perfil, registrar_usuario, SendMessageAPIView, ProtectedView, protected_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('perfil/', perfil, name='perfil_usuario'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Redirige a 'home' después de cerrar sesión
    path('api/registrar/', registrar_usuario, name='registrar_usuario'),
    path('enviar-mensaje/', SendMessageAPIView.as_view(), name='enviar_mensaje'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('api/usuarios/protected/', protected_view, name='protected_view'),
]