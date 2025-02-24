from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.shortcuts import redirect
from .views import update_progress

urlpatterns = [
    path("", views.tasks_view, name="tasks_view"),
    path(
        "update_progress/<int:task_id>/<str:action>",
        update_progress,
        name="update_progress",
    ),
]