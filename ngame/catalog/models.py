from django.db import models
from users.models import User
from datetime import datetime


class Game(models.Model):
    title = models.CharField(max_length=200)
    path = models.ImageField(upload_to="img/%Y/%m/%d/", blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    amount = models.IntegerField()
    date_create = models.DateTimeField(default=datetime.now, blank =True)

    def total_likes(self):
        return Like.objects.filter(game=self).count()
    
    def total_comments(self):
        return Comment.objects.filter(game=self).count()
    
    def user_commented(self, user):
        return Comment.objects.filter(game=self, user=user).exists()
    
    def user_liked(self, user):
        return Like.objects.filter(game=self, user=user).exists()
    
    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'game')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'{self.user} on {self.game}'
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"carrinho do {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def price_total(self):
        return self.quantity * self.game.price 
    
    def __str__(self):
        return f'{self.game} no {self.cart}'
    

class compras(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_create = models.DateTimeField(default=datetime.now, blank =True)

    def __str__(self):
        return f'{self.user} {self.quantity}'

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=200)
    complemento = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    

    def __str__(self):
        return f'{self.user} {self.rua} {self.cidade} {self.cep}'