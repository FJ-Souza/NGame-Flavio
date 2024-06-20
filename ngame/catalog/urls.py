from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('home', home, name='home'),
    path('like/<int:gaming_id>/', like_gaming, name='like_gaming'),
    path('comment/<int:gaming_id>/', comment_gaming, name='comment_gaming'),
    path('add/', add_gaming, name='add_gaming'),
    path('edit/<int:gaming_id>/', edit_gaming, name='edit_gaming'),
    path('delete/<int:gaming_id>/', delete_gaming, name='delete_gaming'),
]