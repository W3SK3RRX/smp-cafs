from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
from manutencoes import views
import re

# Create your views here.


def cadastro(request):
    if request.method == "GET":
        return render(request, "cadastro.html")
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        errors = []

        # Verificação de formato de e-mail
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            errors.append("Formato de e-mail inválido!")

        users = User.objects.filter(username=username)
        if users.exists():
            errors.append("Já existe um usuário com esse nome!")

        verifica_email = User.objects.filter(email=email)
        if verifica_email.exists():
            errors.append("Email já cadastrado!")

        if senha != confirmar_senha:
            errors.append("A senha e o confirmar senha devem ser iguais!")

        if len(senha) < 8:
            errors.append("A senha deve conter mais de 8 caracteres!")

        if not re.search(r"[!@#$%^&*()-_=+{};:,<.>]", senha):
            errors.append("A senha deve conter pelo menos um caractere especial!")

        if not re.search(r"\d", senha):
            errors.append("A senha deve conter pelo menos um número!")

        if not re.search(r"[A-Z]", senha) or not re.search(r"[a-z]", senha):
            errors.append("A senha deve conter pelo menos uma letra maiúscula e uma letra minúscula!")

        if errors:
            for error in errors:
                messages.add_message(request, constants.ERROR, error)
            return redirect('cadastro')

        try:
            User.objects.create_user(
                username=username,
                email=email,
                password=senha
            )
            messages.add_message(request, constants.SUCCESS, "Usuário criado com sucesso! Faça login para continuar.")
            return redirect('login')
        except Exception as e:
            messages.add_message(request, constants.ERROR, f"Ocorreu um erro ao criar o usuário: {e}")
            return redirect('cadastro')


def login(request):
    if request.method=="GET":
        return render(request, "login.html")
    elif request.method=="POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username=username, password=senha)

        if user:
            auth.login(request, user)
            return redirect('/manutencoes/home')
        
        messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos')
        return redirect('login')


def sair(request):
    auth.logout(request)
    return redirect('login')