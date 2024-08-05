from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from catalog.models import *
# Create your views here.


@login_required
def dash(request):
        games = Game.objects.all()
        return render(request, 'dashb/dashboard.html', {'games': games})
    
@login_required
def dash_users(request):
    if request.user.is_superuser:
        users = User.objects.all()
        return render(request, 'dashb/dash_users.html', {'users': users})
    else:
        return redirect ('index')
    
@login_required
def dash_products(request):
    user = request.user    
    games = Game.objects.all()
    data_game = []
    for games in games:
        data_game.append(    
            {
            'games': games,
            'liked': games.user_liked(user) if user.is_authenticated else False,
            'comments': Comment.objects.filter(game=games),
            'commented': games.user_commented(user) if user.is_authenticated else False,
            }
        )
    return render(request, 'dashb/dash_products.html', {'games': data_game})
   

@login_required
def dash_buy(request):
    if request.user.is_superuser:
        buy = compras.objects.all()
        total_buy = buy.count()
        return render(request, 'dashb/dash_buy.html', {'buy': buy, 'total_buy': total_buy})
    else:
        buy = compras.objects.filter(user_id=request.user)
        total_buy = buy.count()
        return render(request, 'dashb/dash_buy.html', {'buy': buy, 'total_buy': total_buy})
   
@login_required
def dash_address(request):
    if request.user.is_superuser:
        cep = Address.objects.all()
        total_address = cep.count()
        return render(request, 'dashb/dash_address.html', {'cep': cep, 'total_address': total_address})
    else:
        
        cep = Address.objects.filter(user_id=request.user)
        total_address = cep.count()
        return render(request, 'dashb/dash_address.html', {'cep': cep, 'total_address': total_address})