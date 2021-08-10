from django.db import models


class Game(models.Model):
    """Game Model
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    designer = models.CharField(max_length=50)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    gameplay_duration = models.IntegerField()
    age_recommendation = models.IntegerField()
    categories = models.ManyToManyField("Category", through="GameCategory")

    def __str__(self):
        return self.title