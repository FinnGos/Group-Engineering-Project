from django.urls import path
from .views import buy_item, shop

urlpatterns = [
    path('buy/item/<int:item_id>/', buy_item, name='buy_item'),
    path('shop/', shop, name='shop'),
]
