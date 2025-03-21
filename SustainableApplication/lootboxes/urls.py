from django.urls import path
from . import views

urlpatterns = [
    path("open/", views.open_lootbox, name="open_lootbox"),
]
