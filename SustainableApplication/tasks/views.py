from django.shortcuts import render
from .models import Tasks
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
import random


# Create your views here.
def tasks_view(request):
    today = now().date()
    incomplete_tasks = list(Tasks.objects.filter(completed=False))

    # retrieve or select random task for today
    if not incomplete_tasks:
        task = None
    else:
        # pick random task once per day
        selected_task = random.choice(incomplete_tasks)

        # reset progress if last update was not today
        if selected_task.updated_at.date() != today:
            selected_task.current_progress = 0
            selected_task.save()

        task = selected_task

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
