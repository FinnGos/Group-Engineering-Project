"""
URL configuration for collectables webpage
"""

from django.urls import path

from . import views


urlpatterns = [
    path("", views.collectable_gallery, name="collectable_gallery"),    
]
