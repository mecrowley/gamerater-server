from django.db import models
from django.contrib.auth.models import User


class GameRating:

    player = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.DO_NOTHING, related_name='pictures')
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return f'Rating for {self.game} by {self.player}'