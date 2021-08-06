from django.db import models

class GameCategory(models.Model):
    """Join model for Games and Categories
    """
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self):
        return f'game: {self.game} category: {self.category}'