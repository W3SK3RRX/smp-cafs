from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
import re

# Create your views here.

def cadastro(request):
    if request.method=="GET":
        return render(request, "cadastro.html")
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        users = User.objects.filter(username=username)

        if users.exists():
            messages.add_message(request, constants.ERROR, "Já existe um usuário com esse nome!")
            return redirect('/usuarios/cadastro')

        verifica_email = User.objects.filter(email=email)

        if verifica_email.exists():
            messages.add_message(request, constants.ERROR, "Email já cadastrado!")
            return redirect('/usuarios/cadastro')
        
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, "A senha e o confirmar senha devem ser iguais!")
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 8:
            messages.add_message(request, constants.ERROR, "A senha deve conter mais de 8 caracteres!")
            return redirect('/usuarios/cadastro')
        
        if not re.search(r"[!@#$%^&*()-_=+{};:,<.>]", senha):
            messages.add_message(request, constants.ERROR, "A senha deve conter pelo menos um caractere especial!")
            return redirect('/usuarios/cadastro')
        
        if not re.search(r"\d", senha):
            messages.add_message(request, constants.ERROR, "A senha deve conter pelo menos um número!")
            return redirect('/usuarios/cadastro')
        
        if not re.search(r"[A-Z]", senha) or not re.search(r"[a-z]", senha):
            messages.add_message(request, constants.ERROR, "A senha deve conter pelo menos uma letra maiúscula e uma letra minúscula!")
            return redirect('/usuarios/cadastro')
        

        try:
            User.objects.create_user(
                username=username,
                email=email,
                password=senha
            )
            return redirect('/usuarios/login')
        except:
            return redirect('/usuarios/cadastro')



def login_view(request):
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
        return redirect('/usuarios/login')


def sair(request):
    auth.logout(request)
    return redirect('/usuarios/login')