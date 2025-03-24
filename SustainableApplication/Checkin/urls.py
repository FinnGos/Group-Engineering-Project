"""This file is used to define the URL patterns for the Checkin app."""
from django.urls import path
from . import views

urlpatterns = [
    path('get_location/<int:task_id>/', views.get_location, name='get_location'),
]
