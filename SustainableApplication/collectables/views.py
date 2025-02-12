from django.shortcuts import render
from django.http import HttpResponse

def display(request):
    return HttpResponse("HTML Stuff")

# Create your views here.
