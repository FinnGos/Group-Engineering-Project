from django.urls import path
from . import views

# Defining URL patterns for the application. Map the URL path 'get location/' view function
urlpatterns = [
    path('TermsAndConditions/', views.get_terms, name='termsAndConditions'),
]
