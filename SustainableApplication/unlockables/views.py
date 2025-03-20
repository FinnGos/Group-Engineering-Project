from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item

@login_required
def buy_item(request, item_id):
    item = Item.objects.get(id=item_id)
    profile = request.user

    if profile.current_points >= item.price:
        profile.current_points -= item.price
        profile.save()
        messages.success(request, f'You bought {item.name}!')
    else:
        messages.error(request, 'Not enough Carbo Coins!')

    return redirect('game_page')  # Redirect to the main game page

@login_required
def shop(request):
    items = Item.objects.all()
    return render(request, 'shop.html', {'items': items})
