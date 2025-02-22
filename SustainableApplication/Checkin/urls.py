from django.urls import path
from . import views

# Defining URL patterns for the application. Map the URL path 'get location/' view function
urlpatterns = [
    path('get_Location/', views.get_location, name='get_location'),
    path('database_location', views.database_location, name='database_location'),
]
