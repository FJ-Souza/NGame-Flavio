from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from users.decorators import user_is_admin, user_is_client
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user_temp = User.objects.get(email= email)
            user = authenticate(username=user_temp, password=password)
            if user is not None:
                login(request, user)
                return redirect('dash_users' if user.user_type == 'admin' else 'dashboard')
            else:
                form.add_error(None, 'invalid username or password')
    return redirect('index')


def register_view(request):
    # if request.method == 'POST':
    #     form = UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Cadastrado com sucesso!')
    #         return redirect('login')
    #     else:
    #         messages.error(request, 'Erro ao cadastrar!')
            
            
    # return redirect('index')
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    return redirect('index')

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
@user_passes_test(user_is_admin)
def admin_page(request):
    return render(request, 'dashb/dash_users.html')

@login_required
@user_passes_test(user_is_client)
def client_page(request):
    return render(request, 'dashb/dashboard.html')