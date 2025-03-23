"""This module contains the views for the unlockables app"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item, Building, UserBuilding, UserItem
import random


@login_required
def buy_item(request, item_id):
    """Function to buy an item from the shop"""
    item = get_object_or_404(Item, id=item_id)
    user = request.user

    # Check if user has enough points
    if user.current_points >= item.price:
        user.current_points -= item.price
        user.save()

        # Place the item
        place_item(user, item)

        # Success message
        messages.success(request, "Purchase successful!")
    else:
        # Error message for insufficient points
        messages.error(request, "Insufficient points to complete the purchase.")

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


def game_map(request):
    """Function to load the game map html

    Args:
        request: The request made to the shop page

    Returns:
        The HTML render for the game map page
    """
    user = request.user
    buildings = Building.objects.all()
    user_buildings = {
        ub.building.id: ub.unlocked for ub in UserBuilding.objects.filter(user=user)
    }
    user_items = UserItem.objects.filter(user=user)

    return render(
        request,
        "map.html",
        {
            "buildings": buildings,
            "user_buildings": user_buildings,
            "user_items": user_items,
        },
    )


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
