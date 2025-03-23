"""This module contains the URL patterns for the tasks app."""
from django.urls import path
from . import views
from .views import update_progress, game_master_gallery, delete_image_game_master

urlpatterns = [
    path("", views.tasks_view, name="tasks_view"),
    path(
        "update_progress/<int:task_id>/<str:action>",
        update_progress,
        name="update_progress",
    ),
    path('tasks/', views.tasks_page, name='tasks_page'), 
    path('upload/<int:task_id>/', views.upload_file, name='upload_file'),
    path('gallery/', views.image_gallery, name='gallery_page'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),  # New delete route
    path('game-master-gallery/', game_master_gallery, name='game_master_gallery'),
    path('delete-image-game-master/<int:image_id>/', delete_image_game_master, name='delete_image_game_master'),

]