"""URL patterns for the PrivacyPolicy application"""
from django.urls import path
from . import views

# Defining URL patterns for the application. Map the URL path 'get location/' view function
urlpatterns = [
    path('PrivacyPolicy/', views.get_privacy, name='privacyPolicy'),
]
