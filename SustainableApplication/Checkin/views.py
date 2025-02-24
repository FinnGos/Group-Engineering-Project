from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Location # Import location model
from geopy.distance import geodesic # pip install required (pip install geopy)
# geopy is used fot geocoding(converting addresses to coordinates)

@login_required
def get_location(request):
    """Method that displays the checkin page and gets the location of the user 

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: checkin_page.html with the location data if valid.
        HttpResponseBadRequest: A 400 response if the latitude or longitude is invalid.
    """
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
        return database_location(request)
        
       # If user doesnt allow us to access their data: 
    context = {
        "message": "We need you to share your location with us to continue playing the game, if you have any concerns about sharing your location with us, you can review our terms and conditions page"
    }
    return render(request, "checkin_page.html", context)


@login_required
def database_location(request):
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

        location_coords = (location.latitude, location.longitude)
        user_coords = (user_lat, user_lon)
        distance = geodesic(location_coords, user_coords).meters

        if distance <= location.radius:
            context = {
                "lat": user_lat,
                "lon": user_lon,
                "message": f"Check-in Succesfull at {location.name}!"
            }
            return render(request, "checkin_page.html", context)
    return HttpResponseBadRequest("You are not in the valid location")
