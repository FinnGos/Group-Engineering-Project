"""Tests for unlockables"""
from django.urls import path
from .views import buy_item, shop, game_map

urlpatterns = [
    path('buy/item/<int:item_id>/', buy_item, name='buy_item'),
    path('shop/', shop, name='shop'),
    path('map/', game_map, name='map'),
]
