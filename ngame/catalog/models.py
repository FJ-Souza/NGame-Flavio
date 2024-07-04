from django.db import models
from users.models import User

class Game(models.Model):
    title = models.CharField(max_length=200)
    path = models.ImageField(upload_to="img/%Y/%m/%d/", blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    amount = models.IntegerField()

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

    def __str__(self):
        return f'{self.game} no {self.cart}'
    