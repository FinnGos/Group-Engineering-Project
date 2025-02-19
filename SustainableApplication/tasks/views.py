from django.shortcuts import render


# Create your views here.
def tasks_view(request):
    context = {}

    return render(request, "tasks.html", context)
