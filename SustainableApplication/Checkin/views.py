from django.http import HttpResponseBadRequest
from django.shortcuts import render


def get_location(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    if lat and lon:
        try:
            lat_true = float(lat)
            lon_true = float(lon)
        except ValueError:
            return HttpResponseBadRequest("Invalid location data.")

        if -180.0 <= lon_true <= 180.0 and -90.0 <= lat_true <= 90.0:
            context = {
                "lat": lat,
                "lon": lon,
                "message": f"Check-In Successful! Lat: {lat}, Lon: {lon}",
            }
            return render(request, "checkin_page.html", context)

        return HttpResponseBadRequest("Invalid location data.")

    return render(request, "checkin_page.html")
