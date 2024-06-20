from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def home(request):
    games = Game.objects.all()
    return render(request, 'catalog/home.html', {'games': games})

# def index(request):
#     games = Game.objects.all()
#     return render(request, 'catalog/index.html', {'games': games})

def index(request):
    user = request.user    
    gaming = Game.objects.all()
    data_game = []
    for games in gaming:
        data_game.append(    
            {
            'games': games,
            'liked': games.user_liked(user) if user.is_authenticated else False,
            'comments': Comment.objects.filter(game=games)
            }
        )
    return render(request, 'catalog/index.html', {'games': data_game})


@login_required
def like_gaming(request, gaming_id):
    gaming = get_object_or_404(Game, id=gaming_id)
    like, created = Like.objects.get_or_create(user=request.user, game=gaming)
    if not created:
        like.delete()
    return redirect('index')

@login_required
def comment_gaming(request, gaming_id):
    gaming = get_object_or_404(Game, id=gaming_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(user=request.user, game=gaming, content=content)
    return redirect('index')

# @login_required
# def detail_gaming(request, gaming_id):
#     gaming = get_object_or_404(Game, id=gaming_id)
#     comments = Comment.objects.filter(gaminging=gaming)
#     liked = False
#     if request.user.is_authenticated:
#         liked = Like.objects.filter(user=request.user, gaming=gaming).exists()
#     return render(request, 'catalog/detail_gaming.html', {'gaming': gaming, 'comments': comments, 'liked': liked})

@login_required
def add_gaming(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jogo cadastrada com sucesso!')
            return redirect('home')
    else:
        form = GameForm()
    return render(request, 'catalog/add_gaming.html', {'form': form})

@login_required
def edit_gaming(request, gaming_id):
    gaming = get_object_or_404(Game, id=gaming_id)
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=gaming)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jogo editada com sucesso!')
            return redirect('home')
    else:
        form = GameForm(instance=gaming)
    return render(request, 'catalog/edit_gaming.html', {'form': form})

@login_required
def delete_gaming(request, gaming_id):
    gaming = get_object_or_404(Game, id=gaming_id)
    if request.method == 'POST':
        gaming.delete()
        messages.success(request, 'Jogo deletada com sucesso!')
        return redirect('home')
    return render(request, 'catalog/delete_gaming.html', {'gaming': gaming})