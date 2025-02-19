from django.http import HttpResponseBadRequest
from django.shortcuts import render

#Handle get requests and extract latitude and longitude
def get_location(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    #if both provided, convert them into floating-point numbers
    if lat and lon:
        try:
            lat_true = float(lat)
            lon_true = float(lon)
            #if data is non-numeric:
        except ValueError:
            return HttpResponseBadRequest("Invalid location data.")
        #check if the longitude and latitude is valid
        #valid values: -180.0 and 180.0 for longitude and -90.0 and 90.0 for latitude
        if -180.0 <= lon_true <= 180.0 and -90.0 <= lat_true <= 90.0:
            context = {
                "lat": lat,
                "lon": lon,
                "message": f"Check-In Successful! Lat: {lat}, Lon: {lon}",
            }
            return render(request, "checkin_page.html", context)
        #if the location data is not in the correct range: 
        return HttpResponseBadRequest("Invalid location data.")
    #   #if user doesnt allow us to acces their data: 
    context = {
        "message": "Unfortunately, we need you to share your location with us to continue playing the game :(, if you have any concerns about sharing your location with us, you can review our terms and conditions page"
    }
    return render(request, "checkin_page.html", context)
