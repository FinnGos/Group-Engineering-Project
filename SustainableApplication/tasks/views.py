from django.shortcuts import render, redirect, get_object_or_404
from .models import Tasks
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import ImageUploadForm
from .models import UploadedImage
import logging
import os
from django.conf import settings

# Set up a logger for authentication events
auth_logger = logging.getLogger("django")


# Define the path to the log file
LOG_FILE_PATH = os.path.join(settings.BASE_DIR, "django_logs.log")


from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
import random


# Create your views here.
@login_required
def tasks_view(request):
    """View to display a maximum of three random incomplete tasks for the user."""
    if not request.user.is_authenticated:
        return render(request, "tasks.html", {"tasks": []})

    user = request.user
    today = now().date()  # Ensure date-only comparison

    # Fetch all incomplete tasks
    incomplete_tasks = list(Tasks.objects.filter(completed=False))

    if incomplete_tasks:
        # Select up to 3 random tasks
        selected_tasks = random.sample(incomplete_tasks, min(3, len(incomplete_tasks)))
    else:
        selected_tasks = []  # No tasks available

    return render(request, "tasks.html", {"tasks": selected_tasks})


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


def upload_file(request, task_id):
    """
    Handles image uploads for a specific task.
    If task_id is 0, create a new task for uploading or redirect to a default task page.
    """
    # Get the list of all daily tasks
    tasks = Tasks.objects.all()  # You can filter if needed

    # If task_id is 0, redirect to task selection
    if task_id == 0:
        task = None
    else:
        task = get_object_or_404(Tasks, id=task_id)

    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]

        uploaded_image = UploadedImage.objects.create(
            task=task, image=image, uploaded_by=request.user
        )
        return redirect("tasks_page")  # Redirect after upload

    return render(request, "upload.html", {"task": task, "tasks": tasks})


@login_required
def tasks_page(request):
    """
    Renders the tasks page with a list of all available tasks.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'tasks.html' template with all tasks.
    """
    tasks = Tasks.objects.all()
    return render(request, "tasks.html", {"tasks": tasks})


@login_required
def image_gallery(request):
    """
    Displays a gallery of all uploaded images linked to tasks.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'gallery.html' template with uploaded images.
    """
    images = UploadedImage.objects.select_related("task")
    return render(request, "task_gallery.html", {"images": images})


@login_required
def delete_image(request, image_id):
    """
    Deletes a specific uploaded image and logs the action.

    Args:
        request (HttpRequest): The HTTP request object.
        image_id (int): The ID of the image to be deleted.

    Returns:
        HttpResponseRedirect: Redirects back to the gallery page.
    """
    image = get_object_or_404(UploadedImage, id=image_id)
    image.delete()
    auth_logger.info(
        f"User {request.user.username} deleted image for Task {image.task.task_name}"
    )
    return redirect("gallery_page")


def is_game_master(user):
    """
    Checks if the given user is the Game Master.

    Args:
        user (User): The user object to check.

    Returns:
        bool: True if the user is the Game Master, otherwise False.
    """
    return user.username == "GameMaster"


@login_required
@user_passes_test(is_game_master)
def game_master_gallery(request):
    """
    Displays the Game Master's gallery, allowing them to view uploaded images by users.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'game_master_gallery.html' template with user selection.
    """
    User = get_user_model()
    users = User.objects.exclude(username="GameMaster")

    selected_user = None
    if request.GET.get("user"):
        try:
            selected_user = User.objects.get(id=request.GET["user"])
        except User.DoesNotExist:
            selected_user = None

    return render(
        request,
        "game_master_gallery.html",
        {
            "users": users,
            "selected_user": selected_user,
        },
    )


@login_required
@user_passes_test(is_game_master)
def delete_image_game_master(request, image_id):
    """
    Allows the Game Master to delete any uploaded image and logs the action.

    Args:
        request (HttpRequest): The HTTP request object.
        image_id (int): The ID of the image to be deleted.

    Returns:
        HttpResponseRedirect: Redirects back to the Game Master gallery.
    """
    image = get_object_or_404(UploadedImage, id=image_id)

    # Check if user is the owner or GameMaster
    if request.user == image.uploaded_by or request.user.username == "GameMaster":
        image.delete()
        auth_logger.info(
            f"User {request.user.username} deleted image for Task {image.task.task_name}"
        )
    else:
        return JsonResponse(
            {"success": False, "message": "Permission denied."}, status=403
        )

    auth_logger.info(
        f"Game Master deleted image for Task {image.task.task_name} uploaded by {image.uploaded_by.username}"
    )

    return redirect("gallery_page")
