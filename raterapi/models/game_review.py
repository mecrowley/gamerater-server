from django.db import models
from django.contrib.auth.models import User


class GameReview:

    player = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.DO_NOTHING, related_name='pictures')
    review = models.TextField()

    def __str__(self):
        return f'Review for {self.game} by {self.player}'