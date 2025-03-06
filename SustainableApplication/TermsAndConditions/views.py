from django.shortcuts import render

"""
Gets Terms and conditions webpage
"""
def get_terms(request):
    return render(request, "terms.html")