from django.shortcuts import render

def get_privacy(request):
    return render(request, "privacy.html")