import random
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from collectables.models import Collectable
from home.models import CustomUser

LOOTBOX_COST = 100
CHANCE = 0.4
REFUND = 60


@login_required
def open_lootbox(request):
    """Picks a random Collectable from the database and adds it to the user's collection if they win"""
    user = request.user  # Get the logged-in user

    if request.method == "POST":
        if user.current_points < LOOTBOX_COST:
            response_data = {
                "success": False,
                "error": "Not enough points to open a lootbox",
                "new_points": user.current_points,
            }
            return JsonResponse(response_data) 

        user.current_points -= LOOTBOX_COST  # Deduct points
        user.save()

        collectables = Collectable.objects.all()  # Get all collectables

        item = None
        is_duplicate = False

        if collectables and random.random() > CHANCE:  # 60% chance to win an item
            item = random.choice(list(collectables))
            if item in user.collectables_owned.all():
                is_duplicate = True
                user.current_points += REFUND # Refund points
            else:
                user.collectables_owned.add(item)  # Add to user's collection

        user.save()

        # Prepare JSON response
        response_data = {
            "success": True,    
            "new_points": user.current_points,  # Always include updated points
            "loot_item": None,
            "is_duplicate": is_duplicate,  # Send duplicate info
        }

        if item:
            response_data["loot_item"] = {
                "name": item.name,
                "image": item.image.url if item.image else "",
                "fact": item.fact,
            }

        return JsonResponse(response_data)

    return render(request, "lootboxes/open_lootbox.html")  # Render page for GET request
