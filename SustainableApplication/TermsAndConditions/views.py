"""This file contains the views for the Terms and Conditions page."""
from django.shortcuts import render

def get_terms(request):
    """Method that displays the terms and conditions page"""
    return render(request, "terms.html")