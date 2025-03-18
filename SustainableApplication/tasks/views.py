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


def tasks_view(request):
    incomplete_tasks = Tasks.objects.filter(completed=False)
    return render(request, "tasks.html", {"tasks": incomplete_tasks})


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



@login_required  # Ensures only logged-in users can upload images
def upload_file(request, task_id):
    """
Handles image uploads for a specific task.

This view allows logged-in users to upload an image associated with a given task. 
If the request method is POST and an image file is provided, the image is saved 
to the database, linked to the task, and the user is redirected to the tasks page.

Args:
    request (HttpRequest): The HTTP request object.
    task_id (int): The ID of the task for which the image is being uploaded.

Returns:
    HttpResponse: Renders the upload page or redirects to the tasks page upon successful upload.
    """
    task = get_object_or_404(Tasks, id=task_id)

    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        
        # Create and save the uploaded image
        uploaded_image = UploadedImage.objects.create(
            task=task, 
            image=image, 
            uploaded_by=request.user
        )
        auth_logger.info(f"User {request.user.username} uploaded an image for Task {task.task_name} (ID: {task.id}). Image filename: {uploaded_image.image.name}")
        return redirect('tasks_page')  # Redirect to the tasks page after upload

    return render(request, 'upload.html', {'task': task})
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
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def image_gallery(request):
    """
    Displays a gallery of all uploaded images linked to tasks.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: Renders the 'gallery.html' template with uploaded images.
    """
    images = UploadedImage.objects.select_related('task')
    return render(request, 'gallery.html', {'images': images})

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
    auth_logger.info(f"User {request.user.username} deleted image for Task {image.task.task_name}")    
    return redirect('gallery_page')

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
    users = User.objects.exclude(username='GameMaster')

    selected_user = None
    if request.GET.get('user'):
        try:
            selected_user = User.objects.get(id=request.GET['user'])
        except User.DoesNotExist:
            selected_user = None

    return render(request, 'game_master_gallery.html', {
        'users': users,
        'selected_user': selected_user,
    })


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
    auth_logger.info(f"Game Master deleted image for Task {image.task.task_name} uploaded by {image.uploaded_by.username}")
    image.delete()

