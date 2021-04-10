from django.shortcuts import render, get_object_or_404

from .models import *


# Create your views here.

def index(request):
    context = {
        "movies": Movie.objects.all()
    }
    return render(request, "homepage.html", context)


def movie(request, id):
    context = {"movie": get_object_or_404(Movie, id=id)}
    return render(request, "movie.html", context)


def advanced_search(request):
    return render(request, "advancedserach.html")
