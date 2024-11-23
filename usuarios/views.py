from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer, PerfilUsuarioSerializer
from usuarios.forms import CustomUserCreationForm
import pika
from django.contrib import messages
from .rabbitmq_client import RabbitMQClient
from usuarios.rabbitmq_client import RabbitMQClient

def home(request):
    return render(request, 'usuarios/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('perfil_usuario')
        else:
            messages.error(request, 'Por favor corrija los errores a continuación.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('perfil_usuario')  # Redirige al perfil del usuario
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'usuarios/login.html')

@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html')

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
def registrar_usuario(request):
    Usuario = get_user_model()
    data = request.data
    usuario = Usuario.objects.create_user(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        rol=data.get('rol', 'huesped')
    )
    enviar_mensaje_rabbitmq(f"Usuario {usuario.username} registrado.")
    return Response({'mensaje': 'Usuario registrado exitosamente'})

class PerfilUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        serializer = PerfilUsuarioSerializer(usuario)
        return Response(serializer.data)

    def put(self, request):
        usuario = request.user
        serializer = PerfilUsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

def enviar_mensaje_rabbitmq(mensaje):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='registro_usuarios')
    channel.basic_publish(exchange='', routing_key='registro_usuarios', body=mensaje)
    connection.close()

class SendMessageAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Obtener datos del cliente
        message_data = request.data

        # Configurar cliente RabbitMQ
        rabbitmq_client = RabbitMQClient(queue_name='mi_cola')

        # Enviar mensaje
        rabbitmq_client.publish_message(message_data)
        rabbitmq_client.close_connection()

        return Response({'status': 'Mensaje enviado a RabbitMQ', 'data': message_data})

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Esto es una vista protegida"})

@api_view(['GET'])
def protected_view(request):
    # Lógica de la vista
    return Response({"message": "Protected endpoint"})