from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Location # Import location model
from Checkin.models import Location
from riddles.models import Riddle
from home.models import CustomUser
from geopy.distance import geodesic # pip install required (pip install geopy)
from django.contrib.auth.decorators import login_required
from tasks.models import Tasks
import logging 
# geopy is used fot geocoding(converting addresses to coordinates)
auth_logger = logging.getLogger("django")


@login_required
def get_location(request, task_id):
    """Method that displays the checkin page and gets the location of the user 

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: checkin_page.html with the location data if valid.
        HttpResponseBadRequest: A 400 response if the latitude or longitude is invalid.
    """

    task = get_object_or_404(Tasks, id=5)

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
    """Checks if the user's location matches a registered location and marks the riddle as completed."""

    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    user_lat = float(lat)
    user_lon = float(lon)

    if not user_lat or not user_lon:
        return HttpResponseBadRequest("Missing location data.")

    locations = Location.objects.using('location_db').all()

    # auth_logger.info("HEREREREREREERER")
    # auth_logger.info(f"Lat: {user_lat}" )
    # auth_logger.info(f"Long: {user_lon}" )

    # auth_logger.info(locations)

    for location in locations:
        # Checking the requested location is within any of the location in the DB locations
        if abs(user_lat - location.latitude) <= 0.001 and abs(user_lon - location.longitude) <= 0.001:
            auth_logger.info(f"Lat of LAT: {user_lat-location.latitude}")
            auth_logger.info(f"Long of LAT: {user_lon - location.longitude}")

            context = {
                "lat": user_lat,
                "lon": user_lon,
                "message": f"Check-in Succesfull at {location.name}!",
            }

            auth_logger.info(location.id)

            try:
                current_location_id = location.id
                riddle = Riddle.objects.get(location_id=current_location_id)
                auth_logger.info(riddle)
            except:
                riddle = None
            
            if riddle != None:# getting into riddle tab by checking the location id is in a riddle
                user = request.user
                user.current_points += 350
                auth_logger.info(request.user.current_points)
                request.user.completed_riddles.add(riddle)
                user.save()
                return render(request, "checkin_page.html", context)

            else:
                #if not then they hae checked into a task and it is completed for that user
                task.has_checked_in = True
                task.save()
                reward = task.reward
                user = request.user
                user.current_points += reward
                user.save()
                auth_logger.info(context)
                return render(request, "checkin_page.html", context)
            

    context = {
            "lat": user_lat,
            "lon": user_lon,
            "message": f"Sorry, you are currently not in the right location",
        }
    return render(request, "checkin_page.html", context)
