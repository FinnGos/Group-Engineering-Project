from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item, Building, UserBuilding, UserItem, Rubbish
import random


@login_required
def buy_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    user = request.user

    # Get the max quantity allowed for this item
    max_quantity = item.max_quantity

    # Count how many of this item the user already owns
    user_item_count = UserItem.objects.filter(user=user, item=item).count()

    if user_item_count >= max_quantity:
        messages.error(request, f"You can't own more than {max_quantity} of {item.name}!")
        return redirect('shop')

    if user.current_points >= item.price:
        user.current_points -= item.price
        user.save()

        # Place the item on the map
        place_item(user, item)

        messages.success(request, f"You bought {item.name} and placed it on the map!")
    else:
        messages.error(request, "Not enough Carbo Coins!")

    return redirect('shop')


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


def game_map(request):
    """Function to load the game map html

    Args:
        request: The request made to the shop page

    Returns:
        The HTML render for the game map page
    """
    user = request.user
    buildings = Building.objects.all()
    rubbish = Rubbish.objects.filter(cleaned=False)  # Only show uncleaned rubbish

    # Get names of collectables the user owns
    unlocked_collectable_names = list(user.collectables_owned.values_list("name", flat=True))

    # Create a dictionary to mark unlocked buildings
    user_buildings = {building.id: (building.name in unlocked_collectable_names) for building in buildings}

    user_items = UserItem.objects.filter(user=user)

    return render(request, "map.html", {
        "buildings": buildings,
        "user_buildings": user_buildings,
        "user_items": user_items,
        "rubbish": rubbish
    })


def place_item(user, item):
    """Function to place the item on the game map making sure it doesn't collide with anything on the map

    Args:
        user: The users that the map belongs to
        item: The item to be placed on the map
    """
    existing_objects = UserItem.objects.filter(user=user)
    map_width, map_height = 1800, 800  # Size of the map
    object_size = 30  # Approximate object size

    while True:
        # Generate random x and y coordinates
        x = random.randint(0, map_width - object_size)
        y = random.randint(0, map_height - object_size)

        # Check if x and y are valid (not None)
        if x is not None and y is not None:
            collision = False
            for obj in existing_objects:
                # Check for collisions with existing objects
                if abs(obj.x - x) < object_size and abs(obj.y - y) < object_size:
                    collision = True
                    break

            if not collision:
                break
        else:
            # If x or y are None, retry generating coordinates
            continue

    # Create a new UserItem with randomly assigned x and y values
    UserItem.objects.create(user=user, item=item, x=x, y=y)

@login_required
def clean_rubbish(request, rubbish_id):
    rubbish = get_object_or_404(Rubbish, id=rubbish_id)

    if rubbish.cleaned:
        messages.info(request, "This rubbish has already been cleaned.")
    elif request.user.current_points >= 5:  # Require 5 Carbo Coins to clean
        request.user.current_points -= 5
        request.user.save()

        rubbish.cleaned = True

        rubbish.save()

        messages.success(request, "You cleaned up some rubbish for 5 Carbo Coins!")
    else:
        messages.error(request, "Not enough Carbo Coins to clean up the rubbish, you need 5 Carbo Coins!")

    return redirect("map")