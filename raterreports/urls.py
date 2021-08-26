from django.urls import path
from .views import top5gameratings_list, bottom5gameratings_list

urlpatterns = [
    path('reports/top5gamesbyrating', top5gameratings_list),
    path('reports/bottom5gamesbyrating', bottom5gameratings_list),
]
