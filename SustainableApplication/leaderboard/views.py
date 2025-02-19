from django.shortcuts import render
from home.models import CustomUser

def leaderboard(request):
    # Order users by points descending, then by username ascending
    users = CustomUser.objects.all().order_by('-all_time_points', 'username')  
    ranked_users = []
    
    last_points = None
    rank = 0
    actual_rank = 0

    for user in users:
        actual_rank += 1
        if user.all_time_points != last_points:
            rank = actual_rank  # Update rank only when points change
        ranked_users.append({'rank': rank, 'user': user})
        last_points = user.all_time_points

    return render(request, 'leaderboard/leaderboard.html', {'ranked_users': ranked_users})
