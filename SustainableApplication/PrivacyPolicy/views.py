from django.shortcuts import render

"""
Gets privacy webpage
"""
def get_privacy(request):
    return render(request, "privacy.html")