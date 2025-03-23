from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item, Building, UserBuilding, UserItem, Rubbish, UserRubbish
import random
from django.utils.timezone import now

@login_required
def buy_item(request, item_id):
    """Fuction that will be called when user clicks button to purchase an item
    will allow them to purchase and place on map or reject

    Args:
        request: Request made to shop HTML
        item_id: id of item to be purchased

    Returns:
        Redirect to the shop HTML
    """
    item = get_object_or_404(Item, id=item_id)
    current_user = request.user

    max_quantity = item.max_quantity
    user_item_count = UserItem.objects.filter(useritem=current_user, item=item).count()


    if user_item_count >= max_quantity:
        messages.error(
            request, f"You can't own more than {max_quantity} of {item.name}!"
        )
        return redirect("shop")

    if current_user.current_points >= item.price:
        current_user.current_points -= item.price
        current_user.all_time_points += item.sustainability_score  # Update sustainability score
        current_user.save()

        place_item(current_user, item)

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
            "all_time_points": current_user.all_time_points,  # Pass all-time sustainability score
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



@login_required
def clean_rubbish(request, rubbish_id):
    """Function that is called when user clicks on button to clean up rubbish

    Args:
        request: The request made to the map page
        rubbish_id: The id of the rubbish pile to be cleaned

    Returns:
        _type_: _description_
    """
    rubbish = get_object_or_404(UserRubbish, id=rubbish_id)
    rubbish_object = get_object_or_404(Rubbish, id=rubbish_id)

    if request.user.current_points >= rubbish.clean_cost:  # Require 5 Carbo Coins to clean
        request.user.current_points -= rubbish.clean_cost
        request.user.save()

        rubbish.cleaned = True
        rubbish.cleaned_at = now()
        rubbish.save()

        request.user.all_time_points -= rubbish_object.sustainability_score
        request.user.save()

        messages.success(request, "You cleaned up some rubbish for 5 Carbo Coins!")
    else:
        messages.error(
            request,
            "Not enough Carbo Coins to clean up the rubbish, you need 5 Carbo Coins!",
        )

    return redirect("map")
