from django.urls import path
from . import views
from .views import leaderboard

urlpatterns = [
    path('', leaderboard, name='leaderboard'),  
]
