"""
URL configuration for collectables webpage
"""

from django.urls import path

from . import views


urlpatterns = [
    path("", views.display, name="display"),    
]
