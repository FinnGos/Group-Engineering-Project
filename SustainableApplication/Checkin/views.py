from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Location # Import location model
from home.models import CustomUser
from geopy.distance import geodesic # pip install required (pip install geopy)
from tasks.models import Tasks
# geopy is used fot geocoding(converting addresses to coordinates)

@login_required
def get_location(request, task_id):
    """Method that displays the checkin page and gets the location of the user 

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: checkin_page.html with the location data if valid.
        HttpResponseBadRequest: A 400 response if the latitude or longitude is invalid.
    """

    task = get_object_or_404(Tasks, id=task_id)

    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    # If both provided, convert them into floating-point numbers
    if lat and lon:
        try:
            user_lat = float(lat)
            user_lon = float(lon)
            # If data is non-numeric:
        except ValueError:
            return HttpResponseBadRequest("Invalid location data.")

        # Check if the coordinates are in the valid range
        if not (-180.0 <= user_lon <= 180.0 and -90.0 <= user_lat <= 90.0):
            return HttpResponseBadRequest("Invalid location data.")
        
        # Redirect to the database_location view for validation
        return database_location(request, task)
        
       # If user doesnt allow us to access their data: 
    context = {
        "message": "We need you to share your location with us to continue playing the game, if you have any concerns about sharing your location with us, you can review our terms and conditions page",
        "task": task
    }
    return render(request, "checkin_page.html", context)


@login_required
def database_location(request, task):
    """Method that checks the user's location to see if it is in the locations database

    
    Args:
        request (HttpRequest): The incoming HTTP request, along with the user's location data.

    Returns:
        HttpResponse: checkin_page.html with the check in successful comment if valid.
        HttpResponseBadRequest: A 400 response if the user is not in a valid location.
    """

    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    user_lat = float(lat)
    user_lon = float(lon)

    if not user_lat or not user_lon:
        return HttpResponseBadRequest("Missing location data.")
    
    # Check locations in the database (location_db)
    locations = Location.objects.using('location_db').all()
    for location in locations:

        if abs(user_lat - location.latitude) <= 0.005 and abs(user_lon - location.longitude) <= 0.005:
            context = {
                "lat": user_lat,
                "lon": user_lon,
                "message": f"Check-in Succesfull at {location.name}!",
                "task":task
            }
            task.has_checked_in = True
            task.save()
            reward = task.reward
            user = request.user
            user.current_points += reward
            user.all_time_points += reward
            user.save()
            return render(request, "checkin_page.html", context)
    context = {
            "lat": user_lat,
            "lon": user_lon,
            "message": f"Sorry, you are currently not in the right location",
            "task": task
        }
    return render(request, "checkin_page.html", context)