from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import CustomUser

@login_required(login_url='/accounts/login/')  # Redirects unauthenticated users
def leaderboard(request):
    # Filter out users with zero points 
    users = CustomUser.objects.filter(all_time_points__gt=0).order_by('-all_time_points', 'username')  

    ranked_users = []
    last_points = None
    rank = 0
    actual_rank = 0

    for user in users:
        actual_rank += 1
        if user.all_time_points != last_points:
            rank = actual_rank
        ranked_users.append({'rank': rank, 'user': user})
        last_points = user.all_time_points

    # Debug: Print ranked_users to check if it's empty
    print("Ranked Users:", ranked_users)

    return render(request, 'leaderboard.html', {'ranked_users': ranked_users})
