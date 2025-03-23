"""This module contains the method that displays the privacy policy page"""
from django.shortcuts import render
def get_privacy(request):
    """Method that displays the privacy policy page"""
    return render(request, "privacy.html")