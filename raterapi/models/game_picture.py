from django.db import models
from django.contrib.auth.models import User


class GamePicture(models.Model):

    player = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.DO_NOTHING, related_name='pictures')
    picture = models.ImageField(
        upload_to='gamepictures', height_field=None,
        width_field=None, max_length=None, null=True)

    def __str__(self):
        return f'Picture of {self.game} uploaded by {self.player}'