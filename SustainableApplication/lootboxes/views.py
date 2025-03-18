import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from collectables.models import Collectable
from home.models import CustomUser


@login_required
def open_lootbox(request):
    """Picks a random Collectable from the database and adds it to the user's collection if they win"""
    user = request.user  # Get the logged-in user
    collectables = Collectable.objects.all()  # Get all collectables

    loot_item = None
    if collectables and random.random() > 0.3:  # 70% chance of getting an item
        loot_item = random.choice(list(collectables))
        if loot_item not in user.collectables_owned.all():
            user.collectables_owned.add(loot_item)  # Add to user's collection

    context = {"loot_item": loot_item}
    return render(request, "lootboxes/open_lootbox.html", context)
