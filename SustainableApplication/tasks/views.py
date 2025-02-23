from django.shortcuts import render
from .models import Tasks
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


# Create your views here.
def tasks_view(request):
    incomplete_tasks = Tasks.objects.filter(completed=False)

    return render(request, "tasks.html", {"tasks": incomplete_tasks})


def update_progress(request, task_id, action):
    task = get_object_or_404(Tasks, id=task_id)

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
