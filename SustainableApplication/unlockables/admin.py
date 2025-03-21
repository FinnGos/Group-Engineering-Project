from django.contrib import admin
from .models import Item, Building, UserBuilding, UserItem

admin.site.register(Item)
admin.site.register(Building)
admin.site.register(UserBuilding)
admin.site.register(UserItem)