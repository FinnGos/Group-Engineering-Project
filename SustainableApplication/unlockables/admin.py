from django.contrib import admin
from .models import Item, Building, UserBuilding, UserItem, Rubbish

admin.site.register(Item)
admin.site.register(Building)
admin.site.register(UserBuilding)
admin.site.register(UserItem)
admin.site.register(Rubbish)