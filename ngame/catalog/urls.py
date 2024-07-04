from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('home', home, name='home'),
    path('like/<int:game_id>/', like_game, name='like_game'),
    path('comment/<int:game_id>/', comment_game, name='comment_game'),
    path('add/', add_game, name='add_game'),
    path('edit/<int:game_id>/', edit_game, name='edit_game'),
    path('delete/<int:game_id>/', delete_game, name='delete_game'),
    path('cart/', view_cart, name='view_cart'),
    path('add_to_cart/<int:game_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_cart/<int:item_id>/', update_cart_item, name='update_cart')
]