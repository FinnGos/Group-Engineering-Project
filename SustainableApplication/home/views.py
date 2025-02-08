from django.shortcuts import render, redirect
from .models import Locations, Collectable, CustomUser
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


# Create your views here.
@login_required
def index(request):
    """view function for home page of site"""

    context = {}

    # render HTML template index.HTML with all data in context variable
    return render(request, "index.html", context=context)


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")

    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


class LoginFormView(LoginView):
    template_name = "registration/login.html"
