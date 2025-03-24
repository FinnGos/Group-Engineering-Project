from django.urls import path
from . import views


urlpatterns = [
    path('', views.riddles_page, name='riddles_page'),
    path('checkin/', views.checkin_page, name='checkin'),
]
