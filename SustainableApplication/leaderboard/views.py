from django.shortcuts import render
from home.models import CustomUser

def leaderboard(request):
    users = CustomUser.objects.all().order_by('-all_time_points')  # Order users by points descending
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

    return render(request, 'leaderboard/leaderboard.html', {'ranked_users': ranked_users})

