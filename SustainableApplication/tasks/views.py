from django.shortcuts import render
from .models import Tasks
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
import random


# Create your views here.
@login_required
def tasks_view(request):
    if not request.user.is_authenticated:
        return render(request, "tasks.html", {"task": None})

    user = request.user
    today = now().date()  # Ensure date-only comparison

    # Get user's existing task if assigned today
    if user.selected_task and user.task_assign_date == today:
        task = user.selected_task
    else:
        user_incomplete_tasks = list(Tasks.objects.filter(completed=False))
        if user_incomplete_tasks:
            task = random.choice(user_incomplete_tasks)
            user.selected_task = task
            user.task_assign_date = today  # Save as date
            user.save(update_fields=["selected_task", "task_assign_date"])
        else:
            task = None  # No tasks available

    return render(request, "tasks.html", {"task": task})


def update_progress(request, task_id, action):
    """Update the progress bar depending on which button is pressed

    Returns:
        JsonResponse: Depending if action is valid, will return update to the web page or an error
    """
    task = get_object_or_404(Tasks, id=task_id)

    # update functions for the claim button and the decrease button
    if action == "increase" and task.current_progress < task.target:
        task.current_progress += 1
    elif action == "decrease" and task.current_progress > 0:
        task.current_progress -= 1
        task.has_checked_in = False
        task.completed = False
    elif (
        action == "claim"
        and task.has_checked_in
        and not task.completed
        and task.current_progress < task.target
    ):

        task.current_progress = task.target
        task.completed = True
    else:
        return JsonResponse(
            {"success": False, "message": "Invalid action or limit reached."}
        )

    task.save()
    return JsonResponse(
        {
            "success": True,
            "new_progress": (task.current_progress / task.target) * 100,
            "current_progress": task.current_progress,
            "target": task.target,
            "completed": task.completed,
        }
    )
