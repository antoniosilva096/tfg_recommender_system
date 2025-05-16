from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import User, Account
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        
        try:
            user = User.objects.create_user(
                username=email,
                email=email, 
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            user.is_active = True
            user.save()

            account = Account(user=user)
            account.save()
            # Enviar correo electrónico (opcional, desactivado por ahora)
            # send_mail(
            #         "Asunto aquí",
            #         "Aquí va el contenido del mensaje.",
            #         "desde@example.com",
            #         ["para@example.com"],
            #         fail_silently=False,
            #     )
            messages.success(request, '¡Registro completado con éxito!')
            return redirect('login')
        except IntegrityError:
            messages.error(request, 'Ya existe un usuario con este correo electrónico.')

    return render(request, 'accounts/register.html')



def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()  # Nombre de usuario o email
        password = request.POST.get('password', '').strip()

        # Validar inputs
        if not identifier or not password:
            messages.error(request, 'Por favor, completa todos los campos.')
            return render(request, 'accounts/login.html')

        # Buscar usuario por nombre de usuario o correo electrónico
        user = User.objects.filter(username=identifier).first() or User.objects.filter(email=identifier).first()

        if user:
            # Autenticar usuario
            authenticated_user = authenticate(request, username=user.username, password=password)
            if authenticated_user:
                if authenticated_user.is_active:
                    auth_login(request, authenticated_user)
                    messages.success(request, 'Has iniciado sesión correctamente.')
                    return redirect('home')  # Cambia 'home' por la página deseada
                else:
                    messages.error(request, 'Tu cuenta no está activa. Contacta al administrador.')
            else:
                messages.error(request, 'Usuario/email o contraseña incorrectos.')
        else:
            messages.error(request, 'Usuario/email o contraseña incorrectos.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.\n ¡Hasta pronto!')
    return redirect('login')

@login_required
def success(request):
    return redirect('home')

@login_required
def perfil(request):
    return render(request, "accounts/perfil.html")
