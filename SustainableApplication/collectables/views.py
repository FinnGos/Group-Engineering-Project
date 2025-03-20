"""
Collection of displays for the collectables webpage
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def collectable_gallery(request):
    """ Displays page of all cards owned by the user from the collectable database"""
    user_object = request.user
    collectables = user_object.collectables_owned.all()

    context = {"collectable_list": collectables}
    return render(request, "gallery.html", context)