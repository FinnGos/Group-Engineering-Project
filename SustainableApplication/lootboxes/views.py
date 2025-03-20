import random
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from collectables.models import Collectable
from home.models import CustomUser

LOOTBOX_COST = 100


@login_required
def open_lootbox(request):
    """Picks a random Collectable from the database and adds it to the user's collection if they win"""
    user = request.user  # Get the logged-in user

    if request.method == "POST":
        if user.current_points < LOOTBOX_COST:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Not enough points to open a lootbox",
                    "new_points": user.current_points,
                },
                status=400,
            )

        user.current_points -= LOOTBOX_COST  # Deduct points
        user.save()  # Save changes

        collectables = Collectable.objects.all()  # Get all collectables

        item = None
        if collectables and random.random() > 0.3:  # 70% chance to win an item
            item = random.choice(list(collectables))
            if item not in user.collectables_owned.all():
                user.collectables_owned.add(item)  # Add to user's collection
                user.save()  # Save changes

        # Prepare JSON response
        response_data = {
            "success": True,
            "new_points": user.current_points,  # Always include updated points
            "loot_item": None,
        }

        if item:
            response_data["loot_item"] = {
                "name": item.name,
                "image": item.image.url if item.image else "",
                "fact": item.fact,
            }

        return JsonResponse(response_data)

    return render(request, "lootboxes/open_lootbox.html")  # Render page for GET request
