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


# def upload_file(request):
#     if request.method == "POST":
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             image = form.save(commit=False)
#             auth_logger.info(f"User {request.user.username} uploaded an image for Task {image.task.task_name}")
#             return redirect('tasks_page')  # Redirect to tasks page after upload
#     else:
#         form = ImageUploadForm()

#     return render(request, 'upload.html', {'form': form})

@login_required  # Ensures only logged-in users can upload images
def upload_file(request, task_id):
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

def tasks_page(request):
    tasks = Tasks.objects.all()
    return render(request, 'tasks.html', {'tasks': tasks})

def image_gallery(request):
    images = UploadedImage.objects.select_related('task')
    return render(request, 'gallery.html', {'images': images})

def delete_image(request, image_id):
    image = get_object_or_404(UploadedImage, id=image_id)
    image.delete()
    auth_logger.info(f"User {request.user.username} deleted image for Task {image.task.task_name}")    
    return redirect('gallery_page')  # Redirect back to the gallery


def is_game_master(user):
    """Check if the user is the Game Master."""
    return user.username == "GameMaster"

@login_required
@user_passes_test(is_game_master)
def game_master_gallery(request):
    # Get all users except for the GameMaster
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
    """Game Master can delete any uploaded image."""
    image = get_object_or_404(UploadedImage, id=image_id)
    auth_logger.info(f"Game Master deleted image for Task {image.task.task_name} uploaded by {image.uploaded_by.username}")
    image.delete()
    #return redirect('game_master_gallery')
    # User = get_user_model() 
    # users = User.objects.exclude(username='GameMaster')
    # selected_user = User.objects.get(id=request.GET['user'])
    # return render(request, 'game_master_gallery.html', {
    #     'users': users,
    #     'selected_user': selected_user,
    # })
    