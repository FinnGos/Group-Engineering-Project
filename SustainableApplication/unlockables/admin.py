from django.contrib import admin
from .models import Item, UserInventory

admin.site.register(Item)
admin.site.register(UserInventory)