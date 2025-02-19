from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.shortcuts import redirect
from tasks import views as tviews


urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("tasks/",tviews.tasks_view, name="task"),
]
