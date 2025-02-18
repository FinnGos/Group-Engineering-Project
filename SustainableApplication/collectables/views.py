"""
Collection of displays for the collectables webpage
"""

from django.shortcuts import render
from .models import Collectable


def display(request):
    """ Displays page of all cards from the collectable database"""
    # Pulls all records from collectable database and sends them to front end
    collectables = Collectable.objects.all()
    context = {"collectable_list": collectables}
    return render(request, "gallery.html", context)

# Create your views here.
