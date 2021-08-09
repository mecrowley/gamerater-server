from django.contrib import admin
from raterapi.models import Category, Game, GameCategory, GamePicture, GameRating, GameReview
# Register your models here.

admin.site.register(Category)
admin.site.register(Game)
admin.site.register(GameCategory)
admin.site.register(GamePicture)
admin.site.register(GameRating)
admin.site.register(GameReview)