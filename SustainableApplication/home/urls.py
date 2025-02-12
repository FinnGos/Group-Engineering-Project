from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.shortcuts import redirect


urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
]
