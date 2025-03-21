from django.urls import path
from . import views

urlpatterns = [
    path('get_location/<int:task_id>/', views.get_location, name='get_location'),
]
