"""This module contains the view function for the leaderboard page of the site."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import CustomUser

@login_required(login_url='/accounts/login/')  # Redirects unauthenticated users
def leaderboard(request):
    """View function for the leaderboard page of the site."""
    # Filter out users with zero points
    users = CustomUser.objects.filter(all_time_points__gt=0).order_by('-all_time_points', 'username') 

    ranked_users = []
    last_points = None
    rank = 0
    actual_rank = 0

    for user in users:
        if user.username == "superadmin" or user.username == "admin":
            continue
        actual_rank += 1
        if user.all_time_points != last_points:
            rank = actual_rank
        ranked_users.append({'rank': rank, 'user': user})
        last_points = user.all_time_points

    # Limit the leaderboard to top 5 users
    ranked_users = ranked_users[:5]
    
    return render(request, 'leaderboard/leaderboard.html', {'ranked_users': ranked_users})
