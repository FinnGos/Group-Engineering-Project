from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
            lat_true = float(lat)
            lon_true = float(lon)
            # If data is non-numeric:
        except ValueError:
            return HttpResponseBadRequest("Invalid location data.")
        # Check if the longitude and latitude is valid
        # Valid values: -180.0 and 180.0 for longitude and -90.0 and 90.0 for latitude
        if -180.0 <= lon_true <= 180.0 and -90.0 <= lat_true <= 90.0:
            context = {
                "lat": lat,
                "lon": lon,
                "message": f"Check-In Successful! Lat: {lat}, Lon: {lon}",
            }
            return render(request, "checkin_page.html", context)
        # If the location data is not in the correct range: 
        return HttpResponseBadRequest("Invalid location data.")
       # If user doesnt allow us to access their data: 
    context = {
        "message": "Unfortunately, we need you to share your location with us to continue playing the game :(, if you have any concerns about sharing your location with us, you can review our terms and conditions page"
    }
    return render(request, "checkin_page.html", context)
