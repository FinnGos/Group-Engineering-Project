
from django.shortcuts import render, redirect
from .models import Locations, Collectable, CustomUser
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

# FOR HASHING PLESAE USE make_password which is a module from django


# Create your views here.
@login_required
def home(request):
    """view function for home page of site

    Returns:
        HTML render template: the HTML page as dictated in the home.html file. Context could be filled
        with data from the database
    """

    context = {}

    # render HTML template index.HTML with all data in context variable
    return render(request, "home.html", context=context)


def signup(request):
    """Method that will be called when user first visits website. will be prompted with a form to login

    Returns:
        HTML render template: depending on whether user selected sign up or login. The signup page or the home page
        will be shown
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # set_password function hashes the password
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect("home")

    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


class LoginFormView(LoginView):
    """Allows us to customize built in login behavior by specifying what template to use. Could add context
    data, redirect users dynamically or log login attempts for analytics.
    """

    template_name = "registration/login.html"
