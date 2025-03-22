from django.urls import path
from .views import buy_item, shop, game_map, clean_rubbish

urlpatterns = [
    path('buy/item/<int:item_id>/', buy_item, name='buy_item'),
    path('shop/', shop, name='shop'),
    path('map/', game_map, name='map'),
    path("clean-rubbish/<int:rubbish_id>/", clean_rubbish, name="clean_rubbish"),  # Add this line
]