from django.db import models
from .game_rating import GameRating


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

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = GameRating.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating

        # Calculate the averge and return it.
        # If you don't know how to calculate averge, Google it.
        average_rating = 0
        if len(ratings) != 0:
            average_rating = total_rating / len(ratings)

        return average_rating

    @average_rating.setter
    def average_rating(self, value):
        self.average_rating = value