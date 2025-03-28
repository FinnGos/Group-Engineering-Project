from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Riddle
from Checkin.models import Location
import datetime

@login_required
def checkin_page(request):
    """
      Handles user check-ins for riddle locations.

    If the location does not exist or has no associated riddle, an error message is returned.

    Args:
        request (HttpRequest): The HTTP request object containing user data and POST parameters.

    Returns:
        HttpResponse: Renders the `checkin_page.html` template with a message indicating success or failure.
    """
    message = ""
    if request.method == "POST":
        location_name = request.POST.get("location")

        try:
            location = Location.objects.get(name=location_name)
            riddle = Riddle.objects.filter(location=location).first()

            if riddle:
                if request.user in riddle.solved_by.all():
                    message = f"You have already solved the riddle at {location.name}!"
                else:
                    riddle.solved_by.add(request.user)  # ✅ Mark as solved for user
                    message = f"Success! You have solved the riddle at {location.name}!"
            else:
                message = "No riddle found at this location."

        except Location.DoesNotExist:
            message = "Invalid location."

    return render(request, 'riddles/checkin_page.html', {'message': message})

def get_current_week():
    """Returns the current week group (1-4) based on a 4-week cycle."""
    current_week = (datetime.date.today().isocalendar()[1] % 4) + 1
    return current_week

@login_required
def riddles_page(request):
    """Display all riddles and check if the user should complete any automatically."""
    
    current_week = get_current_week()
    riddles = Riddle.objects.filter(week_group=current_week)


    return render(request, 'riddles/riddles_page.html', {'riddles': riddles})
