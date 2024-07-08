from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

@login_required
def home(request):
    games = Game.objects.all()
    cart = Cart.objects.filter(user=request.user).first() if request.user.is_authenticated else None
    cart_count = CartItem.objects.filter(cart=cart).count() if request.user.is_authenticated else 0
    return render(request, 'catalog/home.html', {'games': games, "cart_count": cart_count})

def index(request):
    user = request.user
    games = Game.objects.all()
    data_games = []
    cart = Cart.objects.filter(user=request.user).first() if request.user.is_authenticated else None
    cart_count = CartItem.objects.filter(cart=cart).count() if request.user.is_authenticated else 0
    for game in games:
        data_games.append(
            {
                'game': game,
                "liked": game.user_liked(user) if user.is_authenticated else False,
                "commented": game.user_commented(user) if user.is_authenticated else False,
                "comments": Comment.objects.filter(game=game)
            }
        )
    return render(request, 'catalog/index.html', {'games': data_games,"cart_count": cart_count})

@login_required
def like_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    like, created = Like.objects.get_or_create(user=request.user, game=game)
    if not created:
        like.delete()
    return redirect('index')

@login_required
def comment_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(user=request.user, game=game, content=content)
    return redirect('index')


@login_required
def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jogo cadastrado com sucesso!')
            return redirect('home')
    else:
        form = GameForm()
    return render(request, 'catalog/add_game.html', {'form': form})

@login_required
def edit_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jogo editado com sucesso!')
            return redirect('home')
    else:
        form = GameForm(instance=game)
    return render(request, 'catalog/edit_game.html', {'form': form})

@login_required
def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        game.delete()
        messages.success(request, 'Jogo deletado com sucesso!')
        return redirect('home')
    return render(request, 'catalog/delete_game.html', {'game': game})


def add_to_cart(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, game=game, quantity=1)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return JsonResponse({'success': 'true', 'quantity': cart_item.quantity})

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return JsonResponse({'success': 'true'})

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    cart_count = CartItem.objects.filter(cart=cart).count() if request.user.is_authenticated else 0
    total_price = sum( item.quantity * item.game.price for item in items)
    return render(request, 'catalog/cart.html', {'cart': cart, 'items': items, 'cart_count': cart_count, 'total_price': total_price})

def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()
        return JsonResponse({'success': 'true', 'quantity': cart_item.quantity})


def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total_price = sum( item.quantity * item.game.price for item in items)
    if request.method == 'POST':
        cart.delete()
        # termina de fazer o metodo comprar aqui
        messages.success(request, 'Compra realizada com sucesso!')
        return redirect('index')
    return render(request, 'catalog/checkout.html', {'cart': cart, 'total_price': total_price})