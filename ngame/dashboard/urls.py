from django.urls import path
from .views import *

urlpatterns = [
    path('', dash, name='dash'),
    path('users', dash_users, name='dash_users'),
    path('produtos', dash_products, name='dash_products'),
    path('pagamentos', dash_buy, name='dash_buy'),
    path('enderecos', dash_address, name='dash_address'),
   
]