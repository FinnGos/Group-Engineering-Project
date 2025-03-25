"""This module contains the views for the unlockables app"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item, Building, UserBuilding, UserItem, Rubbish, UserRubbish
import random
from django.utils.timezone import now

@login_required
def buy_item(request, item_id):
    """Function that allows the user to purchase an item and place it on the map."""
    
    # Attempt to retrieve the item
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        messages.error(request, "Item not found!")
        return redirect("shop")

    # Get the currently logged-in user
    current_user = request.user

    # Get the maximum quantity allowed for this item
    max_quantity = item.max_quantity

    # Count how many of this item the user already owns
    user_item_count = UserItem.objects.filter(useritem=current_user, item=item).count()

    # Check if the user has reached the maximum allowed quantity
    if user_item_count >= max_quantity:
        messages.error(
            request, f"You can't own more than {max_quantity} of {item.name}!"
        )
        return redirect("shop")

    # Check if the user has enough Carbo Coins to buy the item
    if current_user.current_points >= item.price:
        current_user.current_points -= item.price
        current_user.all_time_points += item.sustainability_score
        current_user.save()

        # Add the item to the user's inventory
        UserItem.objects.create(useritem=current_user, item=item, size=1)  # Default size = 1

        messages.success(request, f"You bought {item.name} and placed it on the map!")
    else:
        messages.error(request, "Not enough Carbo Coins!")

    return redirect("shop")


@login_required
def shop(request):
    """Load the html for the shop webpage

    Args:
        request: The request made to the shop page

    Returns:
        The HTML render for the shop page
    """
    items = Item.objects.all()
    return render(request, "shop.html", {"items": items})

@login_required
def game_map(request):
    """Function to load the game map html

    Args:
        request: The request made to the shop page

    Returns:
        The HTML render for the game map page
    """
    current_user = request.user
    buildings = Building.objects.all()

    # Ensure each user has their own rubbish instances
    all_rubbish = Rubbish.objects.all()
    existing_user_rubbish = UserRubbish.objects.filter(useritem=current_user)

    # Create a set of Rubbish IDs the user already has
    existing_rubbish_ids = set(existing_user_rubbish.values_list("item_id", flat=True))

    new_user_rubbish = []
    for rubbish in all_rubbish:
        if rubbish.id not in existing_rubbish_ids:
            new_user_rubbish.append(UserRubbish(useritem=current_user, item=rubbish))

    # Bulk create new UserRubbish records for efficiency
    if new_user_rubbish:
        UserRubbish.objects.bulk_create(new_user_rubbish)

    # Fetch the UserRubbish instances
    user_rubbish = UserRubbish.objects.filter(useritem=current_user)

    # Check for rubbish respawn
    for record in user_rubbish:
        if record.should_respawn():
            # Reset rubbish for the user
            record.cleaned = False
            record.cleaned_at = None
            record.save()

    # Fetch the UserRubbish instances where cleaned is False
    user_rubbish = UserRubbish.objects.filter(useritem=current_user, cleaned=False)

    # Get the Rubbish instances that correspond to the user's uncleaned rubbish
    rubbish = [ur.item for ur in user_rubbish]

    # Get names of collectables the user owns
    unlocked_collectable_names = list(
        current_user.collectables_owned.values_list("name", flat=True)
    )

    # Create a dictionary to mark unlocked buildings
    user_buildings = {
        building.id: (building.name in unlocked_collectable_names)
        for building in buildings
    }

    # Get all items the user owns
    user_items = UserItem.objects.filter(useritem=current_user)

    return render(
        request,
        "map.html",
        {
            "buildings": buildings,
            "user_buildings": user_buildings,
            "user_items": user_items,
            "rubbish": rubbish,
            "current_points": current_user.current_points,
            "all_time_points": current_user.all_time_points,
        },
    )




def place_item(Current_user, item):
    """Function to place the item on the game map making sure it doesn't collide with anything on the map

    Args:
        Current_user: The user whose map is being updated
        item: The item to be placed on the map
    """
    existing_objects = UserItem.objects.filter(useritem=Current_user)
    existing_buildings = Building.objects.all()
    
    # Collect all occupied positions (from buildings and existing user items)
    occupied_positions = set(
        (building.x, building.y, building.size) for building in existing_buildings
    ) | set(
        (obj.x, obj.y, obj.size) for obj in existing_objects
    )

    map_width, map_height = 1800, 800  # Size of the map

    # Loop to find a non-colliding position
    while True:
        # Generate random x and y coordinates
        x = random.randint(0, map_width - item.size)
        y = random.randint(0, map_height - item.size)

        collision = False
        # Check for collisions with any existing objects (buildings + user items)
        for obj in existing_objects:
            if abs(obj.x - x) < item.size and abs(obj.y - y) < item.size:
                collision = True
                break

        # Also check against building collisions
        for building in existing_buildings:
            if abs(building.x - x) < item.size and abs(building.y - y) < item.size:
                collision = True
                break

        # If no collision, place the item
        if not collision:
            break

    # Create the new UserItem with the free coordinates and the item's size
    UserItem.objects.create(useritem=Current_user, item=item, x=x, y=y, size=item.size)




def clean_rubbish(request, rubbish_id):
    """Function that is called when user clicks on button to clean up rubbish

    Args:
        request: The request made to the map page
        rubbish_id: The id of the rubbish pile to be cleaned

    Returns:
        Redirects back to the map page
    """
    # Get the Rubbish object (the generic type of rubbish)
    rubbish_object = get_object_or_404(Rubbish, id=rubbish_id)

    # Find the specific UserRubbish instance linked to this user and the rubbish type
    user_rubbish = get_object_or_404(UserRubbish, useritem=request.user, item=rubbish_object)

    # Check if user has enough Carbo Coins
    if request.user.current_points >= user_rubbish.clean_cost:
        # Deduct cost
        request.user.current_points -= user_rubbish.clean_cost
        request.user.save()

        # Remove the rubbish instance for the user
        user_rubbish.cleaned = True
        user_rubbish.cleaned_at = now()
        user_rubbish.save()

        # Add sustainability score
        request.user.all_time_points -= rubbish_object.sustainability_score  
        request.user.save()

        messages.success(request, f"You cleaned up Rubbish for {user_rubbish.clean_cost} Carbo Coins!")
    else:
        messages.error(request, f"Not enough Carbo Coins to clean Rubbish! You need {user_rubbish.clean_cost} Carbo Coins.")

    return redirect("map")

